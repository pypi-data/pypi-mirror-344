'''
Validate train config YAML file
'''
from typing import Any, Tuple, List, Dict, Literal, Union, Optional
from pydantic import BaseModel, ValidationError, field_serializer, Field
import json
import yaml
import argparse
import itertools
from tsimpute.core.data import _DataCounterMode, _DataNumGap, _DataGapSize, _DataWindowSize, _DataMissingSpawnMode, _DataVariate
from tsimpute.core.logger import Color, log


def print_validation_error(e: ValidationError):
    errors = e.errors()
    for error in errors:
        _err_loc = '.'.join(map(str, error['loc']))
        print(
            f" {Color.fg.red}({error['type']}){Color.reset} {Color.bold}{_err_loc}{Color.reset} - {error['msg']}")


class SweepConfig(BaseModel):
    hyper_params: List[Any]


class _DatasetConfig(BaseModel):
    name: str
    counter: _DataCounterMode = _DataCounterMode.VALUE
    num_gap: _DataNumGap = Field(1, gt=0)
    gap_size: _DataGapSize = Field(..., gt=0)
    window_size: _DataWindowSize = 'gap_size'
    mode: _DataMissingSpawnMode = 'center'
    variate: Optional[List[Union[str, _DataVariate]]] = None
    missing_value: Any = None

    @field_serializer('counter')
    def serialize_counter(self, value):
        return value.value


class _ProcessConfig(BaseModel):
    name: str
    params: Dict[str, Any] = {}


class _ModelConfig(BaseModel):
    name: Union[str, Literal['dynamic']]
    continuously: bool = False
    params: Dict[str, Any] = {}
    variants: Optional[List[Union[str, '_ModelConfig']]] = None


class _CombinedAlgorithmConfig(BaseModel):
    name: str
    params: Dict[str, Any] = {}


class _MetricConfig(BaseModel):
    name: str
    params: Dict[str, Any] = {}


class _PlotConfig(BaseModel):
    auto_plot: bool = False
    style: Optional[str] = None
    cmap: Optional[str] = None


class _TrainConfig(BaseModel):
    seed: Optional[int] = None
    batch_size: int = 32
    plot: _PlotConfig = _PlotConfig()


class _Experiment(BaseModel):
    dataset: _DatasetConfig
    preprocess: List[Union[str, _ProcessConfig]] = ["outlier", "scaler"]
    models: List[Union[str, _ModelConfig]] = ["lr"]
    combined_algorithms: List[Union[str, _CombinedAlgorithmConfig]] = ["mean"]
    metrics: List[Union[str, _MetricConfig]] = ["similarity"]
    train: _TrainConfig = _TrainConfig()


class Experiments(BaseModel):
    name: str
    description: str = ""
    experiments: List[_Experiment] = []
    image: str = "mingdoan/ts_imputation:latest"
    containers: int = 3
    retries: int = 3


def find_sweeps(config: Dict, path: List = None, sweeps: List = None) -> List[Tuple[List[Union[str, int]], SweepConfig]]:
    if path is None:
        path = []
    if sweeps is None:
        sweeps = []

    if isinstance(config, dict):
        try:
            sweeps.append((path, SweepConfig.model_validate(config)))
        except ValidationError:
            for key, value in config.items():
                find_sweeps(value, path + [key], sweeps)

    elif isinstance(config, list):
        for idx, item in enumerate(config):
            find_sweeps(item, path + [idx], sweeps)

    return sweeps


def build_experiment(config: Dict, sweeps: List[Tuple[List[Union[str, int]], SweepConfig]]):
    # Build all possible combinations
    exps = []
    for _path, _sweep in sweeps:
        exps.append([{
            'path': _path,
            'param': _param
        } for _param in _sweep.hyper_params])
    exps = itertools.product(*exps)

    # Replace hyper params
    for exp in exps:
        _config = config.copy()
        for e in exp:
            _path: List[Union[str, int]] = e['path'][:-1]
            _param = e['param']

            _config_ref = _config
            for _key in _path[:-1]:
                _config_ref = _config_ref[_key]

            _config_ref[_path[-1]] = _param

        yield _config


def build_experiments(configs: List[Dict]) -> Experiments:
    # Define the experiment variables
    experiments = []
    cache_experiment = None

    # Find sweep configs
    for config in configs:
        if cache_experiment is None:
            cache_experiment = Experiments.model_validate(config)

        sweeps = find_sweeps(config)
        exp_gen = build_experiment(config, sweeps)
        for exp in exp_gen:
            experiments.append(_Experiment.model_validate(exp))

    cache_experiment.experiments = experiments
    return cache_experiment


def load_experiments(config_path: str) -> Experiments:
    # Load yaml file
    configs = []
    with open(config_path, 'r') as f:
        _gen = yaml.safe_load_all(f)
        for _config in _gen:
            configs.append(_config)

    return build_experiments(configs)


def validate_config(config_path: str, output_path: str = None):
    log.info("Validating config...")

    # Load yaml file
    configs = []
    with open(config_path, 'r') as f:
        _gen = yaml.safe_load_all(f)
        for _config in _gen:
            configs.append(_config)

    try:
        experiments = build_experiments(configs)
        log.info(
            f"Validated! Found {Color.bold}{len(experiments.experiments)}{Color.reset} experiments")

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(experiments.model_dump(), f, indent=2)
    except ValidationError as e:
        log.error(
            f"Invalid! Found {Color.bold}{len(e.errors())}{Color.reset} errors")
        print_validation_error(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate train config file')
    parser.add_argument('-f', type=str, help='Path to train config file')
    parser.add_argument('-o', type=str, help='Path to output file')
    args = parser.parse_args()

    experiments = validate_config(args.f, args.o)
