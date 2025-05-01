'''
MLFlow wrapper runner
'''

from typing import Optional, List, Dict, Union, Any
import os
import shutil
import datetime
import json
import pandas as pd
import mlflow
from tsimpute.core.validate import _Experiment
from tsimpute.core.alias import load_from_alias
from tsimpute.core.utils import global_seed, get_accelerate_device, GLOBAL_PROPERTIES
from tsimpute.core.data import Data
from tsimpute.core.plot import PlotEngine
from tsimpute.modules.preprocess import Preprocess
from tsimpute.modules.preprocess.base import BaseProcess
from tsimpute.modules.models.base import BaseModel
from tsimpute.modules.combine.base import BaseCombineMethod
from tsimpute.modules.metric import Metrics
from tsimpute.modules.metric.base import BaseMetric
from tsimpute.modules.trainer.base import BaseTrainer, TrainResult
from tsimpute.core.logger import log, Color
from tsimpute.core.config import *


def _exp_verbose(msg: str):
    '''
    Print log message with [Experiment] prefix
    '''
    log.debug(f"{Color.bold}[Experiment]{Color.reset} {msg}")


class MLFlowExperimentWrapper:
    '''
    Wrapper for MLFlow experiment tracking

    Parameters
    ----------
    experiment : _Experiment
        Experiment configuration
    project_name : str
        Project name is Experiment name in MLFlow. Default is 'Default'
    name : str
        Experiment name, aka run name in MLFlow
    description : str
        Experiment description
    author : str
        Experiment author
    data_path : str
        Data path for experiment. If not provided, use data from experiment
    clear : bool
        Clear artifacts directory after experiment
    '''
    DEFAULT_ARTIFACT_DIR = "artifacts"

    def __init__(
        self,
        experiment: _Experiment,
        project_name: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        author: Optional[str] = None,
        data_path: Optional[str] = None,
        clear: bool = False,
        **kwargs
    ):
        # 0. Set variables
        self.experiment = experiment
        self.name = name
        self.description = description
        self.author = author
        self.data_path = data_path
        self.clear = clear
        self.date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.kwargs = kwargs

        # 1. If other project name is provided, create an experiment, else get the default experiment
        if project_name is None:
            project_name = "Default"
        exp = mlflow.get_experiment_by_name(project_name)
        if exp is None:
            exp_id = mlflow.create_experiment(project_name)
            exp = mlflow.get_experiment(exp_id)
        self.exp = exp

        # 2. Init seed & device
        global_seed(experiment.train.seed)
        _exp_verbose(f"Global seed set to {experiment.train.seed}")
        self.device = get_accelerate_device()
        _exp_verbose(f"Accelerate device set to {self.device}")

        # 3. Init data class & load data
        self.data = Data(
            name=experiment.dataset.name,
            counter_mode=experiment.dataset.counter,
            num_gap=experiment.dataset.num_gap,
            gap_size=experiment.dataset.gap_size,
            window_size=experiment.dataset.window_size,
            missing_mode=experiment.dataset.mode,
            data_variate=experiment.dataset.variate,
            missing_value=experiment.dataset.missing_value,
        )
        if self.data_path is not None:
            if self.data_path.startswith("https://") or self.data_path.startswith("http://"):
                self.data.from_url(self.data_path)
            else:
                self.data.from_file(self.data_path)
        else:
            self.data.from_minio(
                object_name=f"{self.experiment.dataset.name}.csv")
        _exp_verbose(f"Data loaded from {self.data_path}")
        GLOBAL_PROPERTIES["Data"] = self.data

        # 4. Init plot engine
        self.ple = PlotEngine(
            plot_style=experiment.train.plot.style,
            cmap=experiment.train.plot.cmap
        )
        GLOBAL_PROPERTIES["PlotEngine"] = self.ple

        # 5. Init preprocess
        preprocess: List[BaseProcess] = []
        for process in experiment.preprocess:
            if isinstance(process, str):
                process = load_from_alias(process)
            else:
                process = load_from_alias(process.name, **process.params)
            preprocess.append(process)
        self.preprocess = Preprocess(preprocess)
        GLOBAL_PROPERTIES["Preprocess"] = self.preprocess

        # 6. Init metrics
        metrics: List[BaseMetric] = []
        for metric in experiment.metrics:
            if isinstance(metric, str):
                metric = load_from_alias(metric)
            else:
                metric = load_from_alias(metric.name, **metric.params)
            metrics.append(metric)
        self.metrics = Metrics(metrics)
        GLOBAL_PROPERTIES["Metrics"] = self.metrics

        # 6. Init models
        self.models: List[BaseModel] = []
        for _model in experiment.models:
            # 6.1. If models is a string, load from alias
            if isinstance(_model, str):
                model = load_from_alias(_model)
            else:
                # 6.2. Check if model config is dynamic
                if _model.name == "dynamic" and _model.variants is not None:
                    # 6.2.1. Load all dynamic models
                    models = []
                    for _m in _model.variants:
                        if isinstance(_m, str):
                            model = load_from_alias(_m)
                        else:
                            model = load_from_alias(_m.name, **_m.params)
                        models.append(model)

                    # 6.2.2. Load dynamic model
                    model = load_from_alias(
                        "dynamic", models=models, **_model.params)
                    model.set_continuous(_model.continuously)

                # 6.3. Load model config from alias
                else:
                    model = load_from_alias(
                        _model.name, **_model.params)
                    model.set_continuous(_model.continuously)

            model.set_device(self.device)
            self.models.append(model)

        # 7. Init combined algorithms
        self.combined_algorithms: List[BaseCombineMethod] = []
        for _method in experiment.combined_algorithms:
            if isinstance(_method, str):
                method = load_from_alias(_method, data=self.data)
            else:
                method = load_from_alias(
                    _method.name, data=self.data, **_method.params)
            self.combined_algorithms.append(method)

        # 8. Init trainer
        trainer_map: Dict[str, List[BaseModel]] = {}
        for model in self.models:
            if model.trainer not in trainer_map:
                trainer_map[model.trainer] = []
            trainer_map[model.trainer].append(model)
        self.trainers = trainer_map

    def __get_value_or_none(self, data: Any, *path: Union[str, int]):
        '''
        Get value from experiment configuration, or return None
        '''
        try:
            value = data
            for p in path:
                value = value[p]
            return value
        except KeyError:
            return None

    def __save_trace_dataframe(self, results: List[TrainResult]):
        '''
        Save trace dataframe to artifacts
        '''
        for result in results:
            df = pd.DataFrame()
            model_name = result["names"][0]
            for i, col in enumerate(self.data.dataframe.columns):
                # Missing data
                df[f"{col}_missing"] = result["traces"]["true"][:, i]
                # Pred
                df[f"{col}_pred"] = result["result"][:, i]
                # Forward
                df[f"{col}_forward"] = result["traces"]["forward"][:, i]
                # Backward
                df[f"{col}_backward"] = result["traces"]["backward"][:, i]
            df.to_csv(os.path.join(self.artifact_path, f"{model_name}.csv"))

    def __run(self, trainer: BaseTrainer):
        '''
        Run experiment with a given trainer, and log results to MLFlow
        '''
        with mlflow.start_run(
            run_name=f"{self.name}_{self.date}",
            experiment_id=self.exp.experiment_id,
            description=self.description,
            tags={
                "author": self.author,
                **self.kwargs
            },
            log_system_metrics=True
        ):
            # 1. Train models
            results = trainer.train()

            # 2. Log results
            for result in results:
                with mlflow.start_run(
                    run_name="_".join(map(str, result["names"])),
                    experiment_id=self.exp.experiment_id,
                    nested=True
                ):
                    # 2.1. Log parameters
                    mlflow.log_params({
                        "data": self.data_path or self.experiment.dataset.name,
                        "model": self.__get_value_or_none(result, "names", 0),
                        "trainer": trainer.__class__.__name__,
                        "combine_method": self.__get_value_or_none(result, "names", 2),
                        "gap_size": self.data.gap_size,
                        "window_size": self.data.window_size,
                        "seed": self.experiment.train.seed,
                    })

                    # 2.2. Log time metrics
                    mlflow.log_metrics({
                        "TrainTime": result["train_time"],
                        "InferTime": result["infer_time"]
                    })

                    # 2.3. Log metrics
                    mlflow.log_metrics({
                        metric["name"]: metric["value"]
                        for metric in result["metrics"]
                    })

            # 3. Save & log artifacts
            self.metrics.get_dataframe().to_csv(
                os.path.join(self.artifact_path, "metrics.csv"))
            self.__save_trace_dataframe(results)
            mlflow.log_artifacts(self.artifact_path)

        # 4. Clear artifacts
        if self.clear:
            shutil.rmtree(self.artifact_path)

    def run(self):
        '''
        Run experiment
        '''

        # 1. Set artifact directory
        self.artifact_path = os.path.join(
            os.getcwd(), self.DEFAULT_ARTIFACT_DIR, self.name, self.date)
        self.ple.set_directory(self.artifact_path)

        # 2. Save data
        self.ple.from_dataframe(self.data.dataframe, name=self.data.name)

        # 3. Preprocess data
        self.preprocess.flow_from_dataframe(
            self.data.dataframe, inplace=True)

        # 4. Export experiment as json
        with open(os.path.join(self.artifact_path, "experiment.json"), "w") as f:
            json.dump(self.experiment.model_dump(), f)

        # 5. Iterate through all trainers
        for _t in self.trainers:
            params = {
                "data": self.data,
                "plot_engine": self.ple,
                "preprocess": self.preprocess,
                "metrics": self.metrics,
                "models": self.trainers[_t],
                "combine_methods": self.combined_algorithms,
                "batch_size": self.experiment.train.batch_size,
                "device": self.device,
                **self.kwargs
            }
            trainer = load_from_alias(_t, **params)
            _exp_verbose(f"Training with {trainer.__class__.__name__}")
            self.__run(trainer)
