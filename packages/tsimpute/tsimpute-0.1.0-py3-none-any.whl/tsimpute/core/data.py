'''
Data loader from blob storage or path
'''
from typing import Any, Union, Literal, List, Optional
import numpy.typing as npt
from enum import Enum
import os
import requests
from pydantic import BaseModel
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from tsimpute.core.logger import log, Color
from tsimpute.core.config import minio_client


def _data_verbose(msg: str):
    '''
    Print log message with [Data] prefix
    '''
    log.debug(f"{Color.bold}[Data]{Color.reset} {msg}")


class _DataError(Exception):
    '''
    Error class for data processing
    '''

    def __init__(self, message: str):
        super().__init__(message)
        log.error(f"{Color.bold}DataError{Color.reset}: " + message)


class _DecomposeMode(str, Enum):
    '''
    Mode of seasonal decomposition
    '''

    ADDITIVE = 'additive'
    MULTIPLICATIVE = 'multiplicative'


class _DataAttribute:
    '''
    Common data attributes for mean, std, min, max, and median
    '''

    def __init__(self, data: pd.DataFrame):
        self.data = data

    @property
    def mean(self) -> npt.NDArray[np.float32]:
        return self.data.mean().to_numpy().squeeze()

    @property
    def std(self) -> npt.NDArray[np.float32]:
        return self.data.std().to_numpy().squeeze()

    @property
    def min(self) -> npt.NDArray[np.float32]:
        return self.data.min().to_numpy().squeeze()

    @property
    def max(self) -> npt.NDArray[np.float32]:
        return self.data.max().to_numpy().squeeze()

    @property
    def median(self) -> npt.NDArray[np.float32]:
        return self.data.median().to_numpy().squeeze()


class _DataCounterMode(str, Enum):
    '''
    Mode of counter for missing data simulation. 
    Count by actual value or data percentage
    '''

    VALUE = 'value'
    PERCENT = 'percent'


_DataNumGap = int
_DataGapSize = Union[int, float]
_DataWindowSize = Union[int, Literal['gap_size']]
_DataMissingSpawnMode = Union[Literal['random'], Literal['center'], str]


class _DataVariate(BaseModel):
    column: str
    is_index: bool = False
    seasonal: Union[int, Literal['auto']] = 'auto'


class Data:
    '''
    Data loader from blob storage or path

    Parameters
    ----------
    counter_mode : _DataCounterMode, optional
        Mode of counter for data point, using actual value or percentage, by default _DataCounterMode.VALUE
    num_gap : _DataNumGap, optional
        Number of missing data gaps, by default 1
    gap_size : _DataGapSize, optional
        Size of missing data gap, by default 1
    window_size : _DataWindowSize, optional
        Size of sliding window for creating training data, by default 'gap_size'
    missing_mode : _DataMissingSpawnMode, optional
        Mode of missing data generation, by default 'center'
    data_variate : List[Union[str, _DataVariate]], optional
        List of data variate for seasonal decomposition, by default None
    missing_value : Any, optional
        Value to replace missing data, by default pd.NA
    auto_datetime : bool, optional
        Automatically convert index to datetime, by default True
    use_detected : bool, optional
        Use detected missing data instead of simulating, by default False
    '''

    def __init__(
        self,
        name: Optional[str] = None,
        counter_mode: Optional[_DataCounterMode] = None,
        num_gap: Optional[_DataNumGap] = None,
        gap_size: Optional[_DataGapSize] = None,
        window_size: Optional[_DataWindowSize] = None,
        missing_mode: Optional[_DataMissingSpawnMode] = None,
        data_variate: Optional[List[Union[str, _DataVariate]]] = None,
        missing_value: Optional[Any] = None,
        auto_datetime: bool = True,
        use_detected: bool = False
    ):
        # Data configurations
        self.name = name
        self.counter = counter_mode or _DataCounterMode.VALUE
        self.num_gap = num_gap or 1
        self.gap_size = gap_size or 1
        self.window_size = window_size or 'gap_size'
        self.mode = missing_mode or 'center'
        self.variate = data_variate
        self.missing_value = missing_value or pd.NA
        self.auto_datetime = auto_datetime
        self.use_detected = use_detected

        # Other configurations
        self.minio_bucket = "datasets"

        # Dataframes
        self.cache_dataframe = None
        self.dataframe = None
        self.decomposed_dataframes = {
            "trend": None,
            "seasonal": None,
            "residual": None
        }
        self.missing_positions: dict[str, list[tuple[Any, Any, int]]] = {}

        _data_verbose(f"Is detect missing: {self.use_detected}")

    def __simulate_missing_validate(self):
        # Check if gap_size is valid
        if self.counter == _DataCounterMode.VALUE:
            if isinstance(self.gap_size, float):
                raise _DataError(
                    "gap_size must be int when counter is 'value'")
        if self.counter == _DataCounterMode.PERCENT:
            if isinstance(self.gap_size, int):
                raise _DataError(
                    "gap_size must be float when counter is 'percent'")

    def __simulate_missing(self):
        if self.dataframe is None:
            return None

        # Iterate through each column
        for _col in self.dataframe.columns:
            self.missing_positions[_col] = []

            # 0.0 Validate parameters
            self.__simulate_missing_validate()

            # 0.1 If counter is PERCENT, calculate gap_size
            if self.counter == _DataCounterMode.PERCENT:
                self.gap_size = int(
                    len(self.dataframe) * self.gap_size)

            # 0.2 Get window size if it is set to gap_size
            if self.window_size == "gap_size":
                self.window_size = self.gap_size

            _data_verbose(
                f"Simulate missing data for column '{_col}' with gap size {self.gap_size} and window size {self.window_size}")

            # 0.3 Set begin, end index, and range
            _begin_index = self.gap_size
            _end_index = len(self.dataframe) - self.gap_size
            _range = (_end_index - _begin_index) // self.num_gap

            # 0.4 Check if number of gaps times with gap size is less than total data
            if (self.num_gap * self.gap_size) + ((self.num_gap - 1) * self.window_size) >= (_end_index - _begin_index):
                raise _DataError(
                    "num_gaps * gap_size must be less than total data")

            _data_verbose(
                f"Simulate mode '{self.mode}' with {_begin_index} to {_end_index} and range {_range}")

            # 1. Simulate missing data by random mode
            if self.mode == "random":
                # 1.1 Iterate through number of gaps
                _begin_select_index = _begin_index
                _end_select_index = _begin_index + _range - self.gap_size
                for _ in range(self.num_gap):
                    # 1.2 Randomly select missing point in range
                    _miss_choice = int(np.random.choice(
                        np.arange(_begin_select_index, _end_select_index)))

                    # 1.3 Add missing point to missing_positions
                    self.missing_positions[_col].append(
                        (_miss_choice, _miss_choice + self.gap_size, self.gap_size))
                    _data_verbose(
                        f"Add missing data from {_miss_choice} to {_miss_choice + self.gap_size}")

                    # 1.4 Update begin and end index
                    if (_miss_choice + self.gap_size + self.window_size) >= _end_index:
                        _begin_select_index = _miss_choice + \
                            self.gap_size + self.window_size
                    else:
                        _begin_select_index = _end_select_index
                    _end_select_index = _end_select_index + _range - self.gap_size

            # 2. Simulate missing data by center mode
            elif self.mode == "center":
                # 2.1 Iterate through number of gaps
                _begin_select_index = _begin_index
                _end_select_index = _begin_index + _range
                for _ in range(self.num_gap):
                    # 2.2 Calculate center index
                    _center_index = (_begin_select_index + _range // 2) - \
                        self.gap_size // 2

                    # 2.3 Add missing point to missing_positions
                    self.missing_positions[_col].append(
                        (_center_index, _center_index + self.gap_size, self.gap_size))
                    _data_verbose(
                        f"Add missing data from {_center_index} to {_center_index + self.gap_size}")

                    # 2.4 Update begin and end index
                    _begin_select_index = _end_select_index
                    _end_select_index = _end_select_index + _range

            # 3. Simulate missing data by start mode
            elif "start" in self.mode:
                # 3.1 Get ofset value if available
                _offset = 0
                _mode = self.mode.split(":")
                if len(_mode) > 1:
                    _offset = int(_mode[1])

                # 3.2 Validate offset
                if _offset >= _range + self.gap_size:
                    raise _DataError(
                        f"Offset must be less than {_range + self.gap_size}")

                # 3.3 Iterate through number of gaps
                _begin_select_index = _begin_index + _offset
                _end_select_index = _begin_index + _range
                for _ in range(self.num_gap):
                    # 3.4 Add missing point to missing_positions
                    self.missing_positions[_col].append(
                        (_begin_select_index, _begin_select_index + self.gap_size, self.gap_size))
                    _data_verbose(
                        f"Add missing data from {_begin_select_index} to {_begin_select_index + self.gap_size}")

                    # 3.5 Update begin and end index
                    _begin_select_index = _end_select_index + _offset
                    _end_select_index = _end_select_index + _range

            # 4. Simulate missing data by end mode
            elif "end" in self.mode:
                # 4.1 Get ofset value if available
                _offset = 0
                _mode = self.mode.split(":")
                if len(_mode) > 1:
                    _offset = int(_mode[1])

                # 4.2 Validate offset
                if _offset >= _range + self.gap_size:
                    raise _DataError(
                        f"Offset must be less than {_range + self.gap_size}")

                # 4.3 Iterate through number of gaps
                _begin_select_index = _begin_index + _range - self.gap_size - _offset
                _end_select_index = _begin_index + _range
                for _ in range(self.num_gap):
                    # 4.4 Add missing point to missing_positions
                    self.missing_positions[_col].append(
                        (_begin_select_index, _begin_select_index + self.gap_size, self.gap_size))
                    _data_verbose(
                        f"Add missing data from {_begin_select_index} to {_begin_select_index + self.gap_size}")

                    # 4.5 Update begin and end index
                    _begin_select_index = _end_select_index + \
                        _range - self.gap_size - _offset
                    _end_select_index = _end_select_index + _range

            else:
                raise _DataError(
                    f"Unsupported mode '{self.mode}'")

        # From missing_positions, create missing data
        for _col, _positions in self.missing_positions.items():
            for _pos in _positions:
                self.dataframe.iloc[_pos[0]:_pos[1],
                                    self.dataframe.columns.get_loc(_col)] = self.missing_value

    def __detect_missing(self):
        if self.dataframe is None:
            return None

        # Find missing data
        for _col in self.dataframe.columns:
            _nan_indices = self.dataframe.index[self.dataframe[_col].isna()]
            _positions = np.arange(len(self.dataframe))[
                self.dataframe[_col].isna()]
            _groups = np.split(_nan_indices, np.where(
                np.diff(_positions) > 1)[0] + 1)
            if len(_groups[0]) > 0:
                self.missing_positions[_col] = [
                    (_group[0], _group[-1], len(_group)) for _group in _groups]

    def __read_csv(self, path: str) -> pd.DataFrame:
        usecols = None
        index_col = 0
        if self.variate:
            if usecols is None:
                usecols = []

            # Load only variate columns
            for v in self.variate:
                # If variate is string, use it as column name
                if isinstance(v, str):
                    usecols.append(v)

                # If variate is object, use it as column name and index
                else:
                    usecols.append(v.column)
                    if v.is_index:
                        index_col = v.column

        # Load data from path
        self.dataframe = pd.read_csv(
            path, na_values=[self.missing_value], usecols=usecols, index_col=index_col)
        self.cache_dataframe = self.dataframe.copy(deep=True)

        # Auto datetime conversion
        if self.auto_datetime:
            try:
                _index = pd.to_datetime(self.dataframe.index, errors='coerce')
                if _index.notna().all():
                    self.dataframe.index = _index
            except Exception as e:
                raise _DataError(
                    f"Failed to convert index to datetime {e}")

    @property
    def config(self):
        return self.__conf

    @property
    def props(self) -> _DataAttribute:
        return _DataAttribute(self.dataframe)

    @property
    def n_features(self):
        if self.dataframe is not None:
            return self.dataframe.shape[1]

    def from_file(self, path: str):
        # Read data from path
        if not os.path.exists(path):
            raise _DataError(f"Path '{path}' can not be retrieved")
        self.__read_csv(path)

        # Perform missing data detection
        if self.use_detected:
            self.__detect_missing()
        else:
            self.__simulate_missing()
        return self

    def from_url(self, url: str):
        # Read data from url
        try:
            response = requests.get(url)
            response.raise_for_status()
            # TODO: Check url reader
            self.__read_csv(response.text)
        except requests.exceptions.RequestException as _:
            raise _DataError(f"Path '{url}' can not be retrieved")

        # Perform missing data detection
        if self.use_detected:
            self.__detect_missing()
        else:
            self.__simulate_missing()
        return self

    def from_minio(self, bucket: str = None, object_name: str = None):
        if not bucket:
            bucket = self.minio_bucket
        if not object_name:
            object_name = f"{self.name}.csv"

        # Read data from minio
        try:
            response = minio_client.get_object(bucket, object_name)
            self.__read_csv(response)
        except Exception as _:
            raise _DataError(
                f"Path '{bucket}/{object_name}' can not be retrieved")

        # Perform missing data detection
        if self.use_detected:
            self.__detect_missing()
        else:
            self.__simulate_missing()
        return self

    def replace_missing_by(self, value: Any = None):
        if self.dataframe is not None:
            if value is None:
                value = self.missing_value
            self.dataframe.replace(
                self.missing_value, value, inplace=True)
        return self

    def decompose(
        self,
        mode: Union[str, _DecomposeMode] = _DecomposeMode.ADDITIVE,
        period: Union[int, dict[str, int]] = 1
    ):
        if self.cache_dataframe is not None:
            # Perform decomposition for each series
            trends, seasonals, residuals = [], [], []
            for column in self.cache_dataframe.columns:
                # Get seasonal value
                _period = None
                if self.variate:
                    for v in self.variate:
                        if isinstance(v, _DataVariate) and v.column == column:
                            if isinstance(v.seasonal, int):
                                _period = v.seasonal
                            break

                # If period is set, override the default value
                if isinstance(period, dict):
                    _period = period.get(column, None)
                if isinstance(period, int):
                    _period = period

                result = seasonal_decompose(
                    self.cache_dataframe[column], model=mode if isinstance(mode, str) else mode.value, period=_period)
                trends.append(result.trend)
                seasonals.append(result.seasonal)
                residuals.append(result.resid)

            # Store decomposed data as dataframe
            self.decomposed_dataframes["trend"] = pd.concat(trends, axis=1)
            self.decomposed_dataframes["seasonal"] = pd.concat(
                seasonals, axis=1)
            self.decomposed_dataframes["residual"] = pd.concat(
                residuals, axis=1)
        return self

    def get_actual_from_missing_index(self, missing_index: int):
        '''
        Get actual data from missing index
        Returns:
            Missing data, shape of data is (n_sample, n_features)
        '''

        if self.cache_dataframe is not None:
            _actuals = []
            for col in self.cache_dataframe.columns:
                _pos = self.missing_positions[col][missing_index]
                _actuals.append(
                    self.cache_dataframe.iloc[_pos[0]:_pos[1], self.cache_dataframe.columns.get_loc(col)].to_numpy())
            return np.array(_actuals).T
        raise _DataError("Dataframe is not loaded")
