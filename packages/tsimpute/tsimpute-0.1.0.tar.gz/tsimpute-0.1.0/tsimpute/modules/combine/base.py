'''
Combination methods for combining imputation results.
'''
from abc import ABCMeta, abstractmethod
import numpy.typing as npt
import numpy as np
from tsimpute.core.logger import log, Color
from tsimpute.core.data import Data


class CombineError(Exception):
    '''
    Common error for combine methods processing
    '''

    def __init__(self, message: str):
        super().__init__(message)
        log.error(f"{Color.bold}CombineError{Color.reset}: {message}")


class BaseCombineMethod(metaclass=ABCMeta):
    '''
    Base class for combination methods.

    Parameters
    ----------
    data: Data
        Data object containing the data and missing position information
    '''

    def __init__(
        self,
        data: Data,
        **kwargs
    ):
        self.data = data
        self.kwargs = kwargs

    def flip_data(self, x: npt.NDArray[np.float32]):
        '''
        Flip data. This method is used to reverse the data.
            x: input data, shape (n_sample, window_size, n_feature)
        '''
        return np.flip(x, axis=1)

    def shape_validation(
        self,
        a: npt.NDArray[np.float32],
        b: npt.NDArray[np.float32]
    ):
        '''
        Check the shape of input data
            a: input data, shape (n_sample, window_size, n_feature)
            b: input data, shape (n_sample, window_size, n_feature)
        '''
        if a.shape != b.shape:
            raise CombineError(
                f"Input data shape must be the same. Got {a.shape} and {b.shape}")

    @abstractmethod
    def combine(
        self,
        forward: npt.NDArray[np.float32],
        backward: npt.NDArray[np.float32],
        current_missing_index: int
    ) -> npt.NDArray[np.float32]:
        '''
        Combine forward and backward data
            forward: forward imputation result, shape (window_size, n_feature)
            backward: backward imputation result, shape (window_size, n_feature)
            current_missing_index: current missing position of the data

        return: combined data, shape (window_size, n_feature)
        '''

    def calculate_train_time(self, train_time: float) -> float:
        '''
        Calculate the training time of the imputation method.
            train_time: training time in seconds

        return: training time in seconds
        '''
        return train_time
    

    def calculate_infer_time(self, infer_time: float) -> float:
        '''
        Calculate the inference time of the imputation method.
            infer_time: inference time in seconds

        return: inference time in seconds
        '''
        return infer_time
