'''
Metrics handling module
'''
from .base import BaseMetric, MetricError, MetricResult
from typing import List, Tuple
import numpy.typing as npt
import numpy as np
import pandas as pd
from tsimpute.core.logger import log, Color

from .common import Similarity, NMAE, RMSE, R2Score, FSD, FB, FA2


def _metric_verbose(msg: str):
    log.debug(f"{Color.bold}[Metric]{Color.reset} {msg}")


def _metric_warning(msg: str, names: Tuple[str]):
    log.warning(f"{Color.bold}[{'.'.join(names)}]{Color.reset} {msg}")


class Metrics:
    '''
    Metrics class for evaluating multiple metrics

    Parameters
    ----------
    metrics: List[BaseMetric]
        List of metrics to evaluate
    use_dataframe: bool
        Use DataFrame to store results
    use_strict: bool
        Raise error if metric value is invalid
    '''

    def __init__(
        self,
        metrics: List[BaseMetric],
        use_dataframe: bool = True,
        use_strict: bool = False
    ):
        self.__metrics = metrics
        self.__use_dataframe = use_dataframe
        self.__use_strict = use_strict

        self.__dataframe = pd.DataFrame(
            columns=['Model', *[metric.__class__.__name__ for metric in metrics]]) if use_dataframe else None

    def __value_validate(self, value: float, metric: BaseMetric, names: Tuple[str]):
        # Check not_greater_than
        if metric.not_greater_than is not None and value > metric.not_greater_than:
            msg = f"{metric.__class__.__name__}: {value} is greater than {metric.not_greater_than}"
            if self.__use_strict:
                raise MetricError(msg)
            else:
                _metric_warning(msg, names)

        # Check not_lower_than
        if metric.not_lower_than is not None and value < metric.not_lower_than:
            msg = f"{metric.__class__.__name__}: {value} is lower than {metric.not_lower_than}"
            if self.__use_strict:
                raise MetricError(msg)
            else:
                _metric_warning(msg, names)

        # Check outlier_warning greater
        if metric.outlier_warning[1] is not None and value > metric.outlier_warning[1]:
            msg = f"{metric.__class__.__name__}: {value} is greater than {metric.outlier_warning[1]}"
            _metric_warning(msg, names)

        # Check outlier_warning lower
        if metric.outlier_warning[0] is not None and value < metric.outlier_warning[0]:
            msg = f"{metric.__class__.__name__}: {value} is lower than {metric.outlier_warning[0]}"
            _metric_warning(msg, names)

    def __add_to_dataframe(self, results: List[MetricResult], names: Tuple[str]):
        if self.__use_dataframe:
            _name = "__".join(names) if len(
                names) > 0 else f"{len(self.__dataframe)}"

            data = {result["name"]: result["value"] for result in results}
            data["Model"] = _name
            self.__dataframe.loc[len(self.__dataframe)] = data

    def evaluate(
        self,
        y_true: npt.NDArray[np.float32],
        y_pred: npt.NDArray[np.float32],
        *names: str
    ) -> List[MetricResult]:
        '''
        Run evaluation on metrics
            y_true: true values, shape (window_size, n_features)
            y_pred: predicted values, shape (window_size, n_features)
            names: names of the evaluation (optional)
        '''

        # 1. Check if y_true and y_pred have the same shape
        if y_true.shape != y_pred.shape:
            raise MetricError(
                f"y_true and y_pred must have the same shape. Got {y_true.shape} and {y_pred.shape}")

        # 2. Iterate over metrics
        results: List[MetricResult] = []
        for metric in self.__metrics:
            # 3. Try to evaluate metric.
            try:
                # 4. Iterate over n_features
                value = 0
                for i in range(y_true.shape[1]):
                    value += metric.evaluate(y_true[:, i], y_pred[:, i])
                value /= y_true.shape[1]

                # 4. Validate value
                self.__value_validate(value, metric, names)

                # 5. Append to results
                results.append(MetricResult(
                    name=metric.__class__.__name__, value=value))
                _metric_verbose(
                    f"Evalutated {metric.__class__.__name__} = {value}")

            except Exception as e:
                raise MetricError(
                    f"Error evaluating {metric.__class__.__name__}: {e}")

        # 6. Return results
        self.__add_to_dataframe(results, names)
        return results

    def get_dataframe(self):
        return self.__dataframe


__all__ = [
    'Metrics',
    'Similarity',
    'NMAE',
    'RMSE',
    'R2Score',
    'FSD',
    'FB',
    'FA2'
]
