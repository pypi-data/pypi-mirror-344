'''
Base class for all metrics
'''

from abc import ABCMeta, abstractmethod
from typing import TypedDict
import numpy.typing as npt
import numpy as np
from tsimpute.core.logger import log, Color


class MetricError(Exception):
    def __init__(self, message):
        super().__init__(message)
        log.error(f"{Color.bold}Metric{Color.reset}: " + message)


class MetricResult(TypedDict):
    '''
    Metric result type
    '''
    name: str
    value: float


class BaseMetric(metaclass=ABCMeta):
    '''
    Base class for metrics

    Attributes
    ----------
    not_greater_than: float
        Metric value should not be greater than this value
    not_lower_than: float
        Metric value should not be lower than this value
    outlier_warning: tuple[float, float]
        Warning if metric value is outside this range
    '''
    not_greater_than: float = None
    not_lower_than: float = None
    outlier_warning: tuple[float, float] = (None, None)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def evaluate(
        self,
        y_true: npt.NDArray[np.float32],
        y_pred: npt.NDArray[np.float32]
    ) -> np.float32:
        '''
        Evaluate the metric
            y_true: true values, shape (window_size, )
            y_pred: predicted values, shape (window_size, )

        return: metric value, float
        '''
