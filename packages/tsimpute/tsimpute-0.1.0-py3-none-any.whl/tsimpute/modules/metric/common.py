'''
Commons for metric module
'''
import numpy as np
from tsimpute.modules.metric.base import BaseMetric


class Similarity(BaseMetric):
    '''
    Similarity metric\n
    `1/T * sum[1, T](1 / (1 + |y_pred - y_true| / (max(y_true) - min(y_true)) ) ) )`

    Higher values are better
    '''
    not_lower_than = 0.0
    not_greater_than = 1.0

    def evaluate(self, y_true, y_pred):
        return np.sum(1 / (1 + np.abs(y_pred - y_true) / (np.max(y_true) - np.min(y_true)))) / y_true.shape[0]


class NMAE(BaseMetric):
    '''
    Normalized Mean Absolute Error metric\n
    `1/T * sum[1, T](|y_pred - y_true| / (max(y_true) - min(y_true)) )`

    Lower values are better
    '''
    not_lower_than = 0.0
    outlier_warning = (-5.0, 5.0)

    def evaluate(self, y_true, y_pred):
        return np.sum(np.abs(y_pred - y_true) / (np.max(y_true) - np.min(y_true))) / y_true.shape[0]


class R2Score(BaseMetric):
    '''
    R² score metric\n
    R² is the square of Pearson's correlation coefficient, measuring the strength of the linear relationship between predicted (y_pred) and actual (y_true) values.\n
    R² = [sum_{i=1}^{T} (y_pred_i - mean(y_pred))(y_true_i - mean(y_true)) / (sqrt(sum_{i=1}^{T} (y_pred_i - mean(y_pred))^2) * sqrt(sum_{i=1}^{T} (y_true_i - mean(y_true))^2))]^2

    Higher values are better
    '''
    not_lower_than = 0.0
    not_greater_than = 1.0

    def evaluate(self, y_true, y_pred):
        # Calculate means
        y_true_mean = np.mean(y_true)
        y_pred_mean = np.mean(y_pred)

        # Calculate the numerator: sum of (y_pred - mean_y_pred) * (y_true - mean_y_true)
        numerator = np.sum((y_pred - y_pred_mean) * (y_true - y_true_mean))

        # Calculate the denominator: product of standard deviations
        y_pred_std = np.sqrt(np.sum((y_pred - y_pred_mean) ** 2))
        y_true_std = np.sqrt(np.sum((y_true - y_true_mean) ** 2))
        denominator = y_pred_std * y_true_std

        # Avoid division by zero
        if denominator == 0:
            return 0.0

        # Calculate Pearson correlation coefficient
        r = numerator / denominator

        # Calculate R² score
        r2 = r ** 2

        return r2


class RMSE(BaseMetric):
    '''
    Root Mean Squared Error metric\n
    `sqrt(1/T * sum[1, T](y_pred - y_true)^2)`

    Lower values are better
    '''
    not_lower_than = 0.0
    outlier_warning = (-5.0, 5.0)

    def evaluate(self, y_true, y_pred):
        return np.sqrt(np.sum((y_pred - y_true) ** 2) / y_true.shape[0])


class FSD(BaseMetric):
    '''
    Fraction of Standard Deviation metric\n
    `2 * (abs(std(y_pred) - str(y_true)) / (std(y_pred) + std(y_true)))`

    Closer to 0 is better
    '''
    not_lower_than = 0.0
    outlier_warning = (None, 5.0)

    def evaluate(self, y_true, y_pred):
        return 2 * (np.abs(np.std(y_pred) - np.std(y_true)) / (np.std(y_pred) + np.std(y_true)))


class FB(BaseMetric):
    '''
    Fraction of Bias metric\n
    `2 * ((mean(y_pred) - mean(y_true)) / (mean(y_pred) + mean(y_true)))`

    Closer to 0 is better. Acceptable range is [-0.3, 0.3]
    '''
    outlier_warning = (-5.0, 5.0)

    def evaluate(self, y_true, y_pred):
        return 2 * ((np.mean(y_pred) - np.mean(y_true)) / (np.mean(y_pred) + np.mean(y_true)))


class FA2(BaseMetric):
    '''
    Fraction of Accuracy metric\n
    `len(0.5 < y_pred / y_true < 2) / T`

    Closer to 1 is better
    '''
    not_lower_than = 0.0
    not_greater_than = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upper_bound = kwargs.get("upper_bound", 2.0)
        self.lower_bound = kwargs.get("lower_bound", 0.5)

    def evaluate(self, y_true, y_pred):
        return np.sum((self.lower_bound < y_pred / y_true) & (y_pred / y_true < self.upper_bound)) / y_true.shape[0]
