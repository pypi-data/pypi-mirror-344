from datetime import datetime
import json
import math
from art.utils.benchmarking.calculate_step_metrics import calculate_step_std_dev
from art.utils.output_dirs import get_model_dir, get_trajectories_split_dir
from art.utils.trajectory_logging import serialize_trajectory_groups
from mp_actors import move_to_child_process
import numpy as np
import os
import polars as pl
import subprocess
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from tqdm import auto as tqdm
from typing import AsyncIterator, cast
import wandb
from wandb.sdk.wandb_run import Run

from .. import dev
from ..api import API
from ..model import Model, TrainableModel
from .service import ModelService
from ..trajectories import Trajectory, TrajectoryGroup
from ..types import Message, TrainConfig
from ..utils import format_message
from .pack import (
    packed_tensors_from_tokenized_results,
    packed_tensors_to_dir,
    PackedTensors,
    plot_packed_tensors,
)
from .tokenize import tokenize_trajectory_groups
from .checkpoints import (
    delete_checkpoints,
    get_step,
    get_last_checkpoint_dir,
)
from .s3_sync import s3_sync


class LocalAPI(API):
    def __init__(self, *, in_process: bool = False, path: str = "./.art") -> None:
        """
        Initializes a local, directory-based API interface at the given path.

        Note:
            The local API uses Weights & Biases for training monitoring.
            If you don't have a W&B account, you can create one at https://wandb.ai.

        Args:
            in_process: Whether to run the local service in-process.
            path: The path to the local directory. Defaults to "./.art".
        """
        self._in_process = in_process
        self._path = path
        os.makedirs(self._path, exist_ok=True)

        # Other initialization
        self._services: dict[str, ModelService] = {}
        self._tokenizers: dict[str, "PreTrainedTokenizerBase"] = {}
        self._wandb_runs: dict[str, Run] = {}

    async def register(
        self,
        model: Model,
    ) -> None:
        """
        Registers a model with the local API for logging and/or training.

        Args:
            model: An art.Model instance.
        """
        output_dir = get_model_dir(self._path, model)
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/model.json", "w") as f:
            json.dump(model.model_dump(), f)

    async def _get_service(self, model: TrainableModel) -> ModelService:
        if model.name not in self._services:
            config = dev.get_model_config(
                base_model=model.base_model,
                output_dir=get_model_dir(self._path, model),
                config=model._internal_config,
            )
            self._services[model.name] = ModelService(
                host="localhost",
                port=8089 + len(self._services),
                model_name=model.name,
                base_model=model.base_model,
                config=config,
                output_dir=get_model_dir(self._path, model),
            )
            if not self._in_process:
                # Kill all "model-service" processes to free up GPU memory
                subprocess.run(["pkill", "-9", "model-service"])
                # To enable sleep mode, import peft before unsloth
                # Unsloth will issue warnings, but everything appears to be okay
                if config.get("engine_args", {}).get("enable_sleep_mode", False):
                    os.environ["IMPORT_PEFT"] = "1"
                # When moving the service to a child process, import unsloth
                # early to maximize optimizations
                os.environ["IMPORT_UNSLOTH"] = "1"
                self._services[model.name] = move_to_child_process(
                    self._services[model.name],
                    process_name="model-service",
                )
        return self._services[model.name]

    def _get_packed_tensors(
        self,
        model: TrainableModel,
        trajectory_groups: list[TrajectoryGroup],
        plot_tensors: bool,
    ) -> PackedTensors | None:
        if not model.base_model in self._tokenizers:
            self._tokenizers[model.base_model] = AutoTokenizer.from_pretrained(
                model.base_model
            )
        tokenizer = self._tokenizers[model.base_model]
        tokenized_results = list(
            tokenize_trajectory_groups(
                tokenizer,
                trajectory_groups,
            )
        )
        if not tokenized_results:
            return None
        max_tokens = max(len(result.tokens) for result in tokenized_results)
        # Round up max_tokens to the nearest multiple of 2048
        sequence_length = math.ceil(max_tokens / 2048) * 2048
        packed_tensors = packed_tensors_from_tokenized_results(
            tokenized_results,
            sequence_length,
            pad_token_id=tokenizer.eos_token_id,  # type: ignore
        )
        # If all logprobs are NaN then there is no suitable data for tuning
        if np.isnan(packed_tensors["logprobs"]).all():
            print(
                "There are no assistant logprobs to train on. Did you forget to include at least one Choice in Trajectory.messages_and_choices?"
            )
            return None
        if plot_tensors:
            plot_packed_tensors(packed_tensors)
        else:
            print(
                f"Packed {len(tokenized_results)} trajectories into {packed_tensors['tokens'].shape[0]} sequences of length {packed_tensors['tokens'].shape[1]}"
            )
        return packed_tensors

    async def _get_step(self, model: TrainableModel) -> int:
        return self.__get_step(model)

    def __get_step(self, model: TrainableModel) -> int:
        return get_step(get_model_dir(self._path, model))

    async def _delete_checkpoints(
        self,
        model: TrainableModel,
        benchmark: str,
        benchmark_smoothing: float,
    ) -> None:
        output_dir = get_model_dir(self._path, model)
        # Keep the latest step
        steps_to_keep = [get_step(output_dir)]
        try:
            best_step = (
                pl.read_ndjson(f"{output_dir}/history.jsonl")
                .drop_nulls(subset=[benchmark])
                .group_by("step")
                .mean()
                .with_columns(pl.col(benchmark).ewm_mean(alpha=benchmark_smoothing))
                .sort(benchmark)
                .select(pl.col("step").last())
                .item()
            )
            steps_to_keep.append(best_step)
        except FileNotFoundError:
            pass
        except pl.exceptions.ColumnNotFoundError:
            print(f'No "{benchmark}" metric found in history')
        delete_checkpoints(output_dir, steps_to_keep)

    async def _prepare_backend_for_training(
        self,
        model: TrainableModel,
        config: dev.OpenAIServerConfig | None = None,
    ) -> tuple[str, str]:
        service = await self._get_service(model)
        await service.start_openai_server(config=config)
        server_args = (config or {}).get("server_args", {})

        base_url = f"http://{server_args.get('host', '0.0.0.0')}:{server_args.get('port', 8000)}/v1"
        api_key = server_args.get("api_key", None) or "default"

        return base_url, api_key

    async def _log(
        self,
        model: Model,
        trajectory_groups: list[TrajectoryGroup],
        split: str = "val",
    ) -> None:
        # Save logs for trajectory groups
        parent_dir = get_trajectories_split_dir(get_model_dir(self._path, model), split)
        os.makedirs(parent_dir, exist_ok=True)

        # Get the file name for the current iteration, or default to 0 for non-trainable models
        iteration = self.__get_step(model) if isinstance(model, TrainableModel) else 0
        file_name = f"{iteration:04d}.yaml"

        # Write the logs to the file
        with open(f"{parent_dir}/{file_name}", "w") as f:
            f.write(serialize_trajectory_groups(trajectory_groups))

        # Collect all metrics (including reward) across all trajectories
        all_metrics: dict[str, list[float]] = {"reward": [], "exception_rate": []}

        for group in trajectory_groups:
            for trajectory in group:
                if isinstance(trajectory, BaseException):
                    all_metrics["exception_rate"].append(1)
                    continue
                else:
                    all_metrics["exception_rate"].append(0)
                # Add reward metric
                all_metrics["reward"].append(trajectory.reward)

                # Collect other custom metrics
                for metric, value in trajectory.metrics.items():
                    if metric not in all_metrics:
                        all_metrics[metric] = []
                    all_metrics[metric].append(value)

        # Calculate averages for all metrics
        averages = {}
        for metric, values in all_metrics.items():
            if len(values) > 0:
                averages[metric] = sum(values) / len(values)

        # Calculate average standard deviation of rewards within groups
        averages["reward_std_dev"] = calculate_step_std_dev(trajectory_groups)

        if isinstance(model, TrainableModel):
            self._log_metrics(model, averages, split)

    def _trajectory_log(self, trajectory: Trajectory) -> str:
        """Format a trajectory into a readable log string."""
        header = f"reward: {trajectory.reward} {' '.join(f'{k}: {v}' for k, v in trajectory.metrics.items())}\n\n"
        formatted_messages = []
        for message_or_choice in trajectory.messages_and_choices:
            if isinstance(message_or_choice, dict):
                message = message_or_choice
            else:
                message = cast(Message, message_or_choice.message.model_dump())
            formatted_messages.append(format_message(message))
        return header + "\n".join(formatted_messages)

    async def _train_model(
        self,
        model: TrainableModel,
        trajectory_groups: list[TrajectoryGroup],
        config: TrainConfig,
        dev_config: dev.TrainConfig,
    ) -> AsyncIterator[dict[str, float]]:
        service = await self._get_service(model)
        await self._log(model, trajectory_groups, "train")
        packed_tensors = self._get_packed_tensors(
            model, trajectory_groups, plot_tensors=False
        )
        if packed_tensors is None:
            print(
                "Skipping tuning as there is no suitable data. "
                "This can happen when all the trajectories in the same group "
                "have the same reward and thus no advantage to train on."
            )
            return
        disk_packed_tensors = packed_tensors_to_dir(
            packed_tensors, f"{get_model_dir(self._path, model)}/tensors"
        )
        results: list[dict[str, float]] = []
        num_gradient_steps = disk_packed_tensors["num_sequences"]
        pbar = tqdm.tqdm(total=num_gradient_steps, desc="train")
        async for result in service.train(disk_packed_tensors, config, dev_config):
            results.append(result)
            yield {**result, "num_gradient_steps": num_gradient_steps}
            pbar.update(1)
            pbar.set_postfix(result)
        pbar.close()
        data = {
            k: sum(d.get(k, 0) for d in results) / sum(1 for d in results if k in d)
            for k in {k for d in results for k in d}
        }
        self._log_metrics(model, data, "train", step_offset=-1)

    def _log_metrics(
        self,
        model: TrainableModel,
        metrics: dict[str, float],
        split: str,
        step_offset: int = 0,
    ) -> None:
        # Add namespacing if needed
        metrics = (
            {f"{split}/{metric}": value for metric, value in metrics.items()}
            if split
            else metrics
        )
        step = (
            self.__get_step(model) if isinstance(model, TrainableModel) else 0
        ) + step_offset

        # If we have a W&B run, log the data there
        if run := self._get_wandb_run(model):
            run.log(
                metrics,
                step=step,
            )

    def _get_wandb_run(self, model: TrainableModel) -> Run | None:
        if "WANDB_API_KEY" not in os.environ:
            return None
        if (
            model.name not in self._wandb_runs
            or self._wandb_runs[model.name]._is_finished
        ):
            run = wandb.init(
                project=model.project,
                name=model.name,
                id=model.name,
                resume="allow",
            )
            self._wandb_runs[model.name] = run
        return self._wandb_runs[model.name]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_s3_path(
        *,
        s3_bucket: str,
        prefix: str | None,
        project: str,
        model: str,
    ) -> str:
        """Return the fully-qualified S3 URI for this model directory."""
        prefix_part = f"{prefix.strip('/')}/" if prefix else ""
        return f"s3://{s3_bucket}/{prefix_part}{project}/models/{model}"

    async def _experimental_pull_from_s3(
        self,
        model: Model,
        *,
        s3_bucket: str,
        prefix: str | None = None,
        verbose: bool = False,
        delete: bool = False,
    ) -> None:
        """Download the model directory from S3 into local API storage. Right now this can be used to pull trajectory logs for processing."""
        local_dir = get_model_dir(self._path, model)
        os.makedirs(local_dir, exist_ok=True)
        s3_path = self._build_s3_path(
            s3_bucket=s3_bucket,
            prefix=prefix,
            project=model.project,
            model=model.name,
        )
        await s3_sync(s3_path, local_dir, verbose=verbose, delete=delete)

        if isinstance(model, TrainableModel):
            service = await self._get_service(model)
            lora_path = get_last_checkpoint_dir(local_dir)
            if lora_path is not None:
                service._set_lora(lora_path)

    async def _experimental_push_to_s3(
        self,
        model: Model,
        *,
        s3_bucket: str,
        prefix: str | None = None,
        verbose: bool = False,
        delete: bool = False,
    ) -> None:
        """Upload the model directory from local storage to S3."""
        local_dir = get_model_dir(self._path, model)
        s3_path = self._build_s3_path(
            s3_bucket=s3_bucket,
            prefix=prefix,
            project=model.project,
            model=model.name,
        )
        await s3_sync(local_dir, s3_path, verbose=verbose, delete=delete)
