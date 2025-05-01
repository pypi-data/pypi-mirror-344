'''
Preprocess module
'''
from typing import List
import pandas as pd
import numpy.typing as npt
import numpy as np
from tsimpute.core.logger import log, Color
from tsimpute.modules.preprocess.base import BaseProcess, PreprocessError

from .outlier import OutlierRemoval
from .scaler import Scaler


def _process_verbose(msg: str):
    '''
    Print verbose message for preprocess
    '''
    log.debug(f"{Color.bold}[Preprocess]{Color.reset} {msg}")


class Preprocess:
    def __init__(self, processes: List[BaseProcess]):
        self.__processes = processes

    def flow_from_dataframe(
        self,
        data: pd.DataFrame,
        inplace: bool = False
    ) -> pd.DataFrame:
        # 1. Check if data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            raise PreprocessError("input must be a pandas DataFrame")

        # 2. Apply processes
        for process in self.__processes:
            _process_verbose(f"Applying {process.__class__.__name__}")

            if process.use_numpy:
                if inplace:
                    data.iloc[:, :] = process.flow(data.to_numpy())
                else:
                    data = pd.DataFrame(
                        process.flow(data.to_numpy()),
                        columns=data.columns,
                        index=data.index
                    )
            else:
                data = process.flow(data)

        return data

    def flow_from_numpy(
        self,
        data: npt.NDArray[np.float32]
    ) -> npt.NDArray[np.float32]:
        # 1. Check if data is a numpy array
        if not isinstance(data, np.ndarray):
            raise PreprocessError("input must be a numpy array")

        # 2. Apply processes
        for process in self.__processes:
            _process_verbose(f"Applying {process.__class__.__name__}")
            data = process.flow(data)

        return data

    def reverse_from_dataframe(
        self,
        data: pd.DataFrame,
        inplace: bool = False
    ) -> pd.DataFrame:
        # 1. Check if data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            raise PreprocessError("input must be a pandas DataFrame")

        # 2. Apply processes in reverse order
        for process in self.__processes[::-1]:
            _process_verbose(f"Reversing {process.__class__.__name__}")

            if process.use_numpy:
                if inplace:
                    data.iloc[:, :] = process.reverse(data.to_numpy())
                else:
                    data = pd.DataFrame(
                        process.reverse(data.to_numpy()),
                        columns=data.columns,
                        index=data.index
                    )
            else:
                data = process.reverse(data)

        return data

    def reverse_from_numpy(
        self,
        data: npt.NDArray[np.float32]
    ) -> npt.NDArray[np.float32]:
        # 1. Check if data is a numpy array
        if not isinstance(data, np.ndarray):
            raise PreprocessError("input must be a numpy array")

        # 2. Apply processes in reverse order
        for process in self.__processes[::-1]:
            _process_verbose(f"Reversing {process.__class__.__name__}")
            data = process.reverse(data)

        return data


__all__ = [
    'Preprocess',
    'OutlierRemoval',
    'Scaler'
]
