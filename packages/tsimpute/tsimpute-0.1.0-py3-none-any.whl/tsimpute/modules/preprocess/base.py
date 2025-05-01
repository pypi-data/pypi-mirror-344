'''
Base preprocessing class
'''
from typing import Union, Any
import numpy.typing as npt
import pandas as pd
from tsimpute.core.logger import log, Color


_DataFrameOrArray = Union[pd.DataFrame, npt.NDArray[Any]]


class PreprocessError(Exception):
    '''
    Common error for preprocess methods processing
    '''

    def __init__(self, message):
        super().__init__(message)
        log.error(f"{Color.bold}Preprocess{Color.reset}: " + message)


class BaseProcess:
    '''
    Base class for preprocessing

    Attributes
    ----------
    use_numpy: bool
        Use numpy array instead of DataFrame
    '''

    def __init__(self):
        self.use_numpy: bool = False

    def flow(self, data: _DataFrameOrArray) -> _DataFrameOrArray:
        '''
        Flow data through the process.
            If use_numpy is True, data will be a numpy array with shape (n_samples, n_features).
            If use_numpy is False, data will be a DataFrame.
        '''
        return data

    def reverse(self, data: _DataFrameOrArray) -> _DataFrameOrArray:
        '''
        Reverse data through the process.
            If use_numpy is True, data will be a numpy array with shape (n_samples, n_features).
            If use_numpy is False, data will be a DataFrame.
        '''
        return data
