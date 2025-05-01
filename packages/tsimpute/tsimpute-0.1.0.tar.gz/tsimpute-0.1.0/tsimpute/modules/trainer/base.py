'''
Base trainer for all trainers
'''
from typing import List, TypedDict, Dict, Any
from abc import ABCMeta, abstractmethod
from tsimpute.core.data import Data
from tsimpute.core.plot import PlotEngine
from tsimpute.modules.preprocess import Preprocess
from tsimpute.modules.models.base import BaseModel
from tsimpute.modules.metric import Metrics, MetricResult


class TrainResult(TypedDict):
    names: List[str]
    result: Any
    train_time: float
    infer_time: float
    metrics: List[MetricResult]
    traces: Dict[str, Any]
    paths: Dict[str, Any]


class BaseTrainer(metaclass=ABCMeta):
    '''
    Base trainer for all trainers

    Parameters
    ----------
    data : Data
        Data object
    plot_engine : PlotEngine
        Plot engine object
    preprocess : Preprocess
        Preprocess object
    metrics : Metrics
        Metrics object
    models : List[BaseModel]
        List of models
    **kwargs
        Additional arguments
    '''

    def __init__(
        self,
        data: Data,
        plot_engine: PlotEngine,
        preprocess: Preprocess,
        metrics: Metrics,
        models: List[BaseModel],
        **kwargs
    ):
        self.data = data
        self.plot_engine = plot_engine
        self.preprocess = preprocess
        self.models = models
        self.metrics = metrics
        self.kwargs = kwargs

    @abstractmethod
    def train(self, **kwargs) -> List[TrainResult]:
        '''
        Train models with given experiment configuration
        '''
        raise NotImplementedError
