'''
Bi-Directional trainer
'''
from typing import List, Tuple, Generator, Union, Optional
import numpy.typing as npt
import time
import numpy as np
import torch
from tsimpute.modules.trainer.base import BaseTrainer, TrainResult
from tsimpute.core.data import Data
from tsimpute.core.plot import PlotEngine
from tsimpute.core.logger import log, Color
from tsimpute.core.utils import get_accelerate_device
from tsimpute.modules.preprocess import Preprocess
from tsimpute.modules.metric import Metrics
from tsimpute.modules.models.base import BaseBiDirectionalModel
from tsimpute.modules.combine.base import BaseCombineMethod


def _train_verbose(msg: str):
    '''
    Print verbose message for training process
    '''
    log.debug(f"{Color.bold}[BiDirectionalTrainer]{Color.reset} {msg}")


_TensorType = Union[npt.NDArray[np.float32], torch.Tensor]
_TransformedData = Tuple[_TensorType, _TensorType]


class DataTransformer:
    '''
    Transforming data for time series forecasting.
    Handles windowing, batching, and conversion to PyTorch tensors.
    '''

    def __init__(
        self,
        data: npt.NDArray[np.float32],
        window_size: int,
        batch_size: int,
        device: torch.device,
        dtype: torch.dtype,
        step_size: int = 1,
        tensor_cast: bool = False
    ):
        """
        Initialize the DataTransformer.

        Args:
            data: Input data with shape (n_samples, n_features)
            window_size: Size of the sliding window
            batch_size: Number of samples per batch
            device: PyTorch device to place tensors on
            dtype: PyTorch data type for the tensors
            step_size: Stride for the sliding window
            tensor_cast: Whether to convert numpy arrays to PyTorch tensors
        """
        self.data = data
        self.window_size = window_size
        self.batch_size = batch_size
        self.device = device
        self.dtype = dtype
        self.step_size = step_size
        self.tensor_cast = tensor_cast

    def __len__(self) -> int:
        """
        Returns the number of available windows in the dataset.
        """
        return (self.data.shape[0] - self.window_size - 1) // self.step_size

    def __getitem__(self, idx: Union[int, slice, List[int], np.ndarray]) -> _TransformedData:
        """
        Get a window or batch of windows from the dataset.

        Args:
            idx: Can be:
                - An integer for a single window
                - A slice object for a range of windows
                - A list or array of specific indices

        Returns:
            _TransformedData with x and y components, where:
                - x is the window(s) of shape (window_size, n_features) or (batch_size, window_size, n_features)
                - y is the target value(s) after the window of shape (n_features) or (batch_size, n_features)
        """
        # 1. Validate dataset has enough samples
        n_samples = self.data.shape[0]
        if n_samples <= self.window_size:
            raise ValueError(
                f"Data has {n_samples} samples, need at least {self.window_size + 1}")

        # 2. Handle different types of indexing
        if isinstance(idx, int):
            # Single item case
            if idx < 0 or idx >= len(self):
                raise IndexError(
                    f"Index {idx} out of range for dataset with length {len(self)}")

            # Calculate the actual starting position
            start_idx = idx * self.step_size

            # Extract window and target
            x = self.data[start_idx:start_idx + self.window_size]
            y = self.data[start_idx + self.window_size]

            # Convert to tensor if required
            if self.tensor_cast:
                x = torch.tensor(x, dtype=self.dtype, device=self.device)
                y = torch.tensor(y, dtype=self.dtype, device=self.device)

            return x, y

        # 3. Handle batch access (slice or list)
        if isinstance(idx, slice):
            # Convert slice to list of indices
            start = 0 if idx.start is None else max(0, idx.start)
            stop = len(self) if idx.stop is None else min(len(self), idx.stop)
            step = 1 if idx.step is None else idx.step
            indices = list(range(start, stop, step))
        else:
            # Assume idx is an iterable of indices
            indices = [i for i in idx if 0 <= i < len(self)]

        # Handle empty batch
        if not indices:
            raise IndexError("Empty batch requested")

        # 4. Extract windows and targets for the batch
        batch_size = len(indices)
        n_features = self.data.shape[1]

        # Create arrays to hold the batch data
        x_batch = np.zeros((batch_size, self.window_size,
                           n_features), dtype=self.data.dtype)
        y_batch = np.zeros((batch_size, n_features), dtype=self.data.dtype)

        # Fill the batch arrays
        for i, idx in enumerate(indices):
            start_idx = idx * self.step_size
            x_batch[i] = self.data[start_idx:start_idx + self.window_size]
            y_batch[i] = self.data[start_idx + self.window_size]

        # 5. Convert to tensor if required
        if self.tensor_cast:
            x_batch = torch.tensor(
                x_batch, dtype=self.dtype, device=self.device)
            y_batch = torch.tensor(
                y_batch, dtype=self.dtype, device=self.device)

        return x_batch, y_batch

    def __iter__(self):
        """
        Generator that yields batches of data windows and their corresponding targets.
        Each batch contains at most self.batch_size windows.
        """
        num_batches = (len(self) + self.batch_size -
                       1) // self.batch_size  # Ceiling division

        for batch_idx in range(num_batches):
            # Calculate start and end indices for this batch
            start_idx = batch_idx * self.batch_size
            end_idx = min(start_idx + self.batch_size, len(self))

            # Get the batch using __getitem__
            yield self[slice(start_idx, end_idx)]

    def __call__(self) -> _TransformedData:
        """
        Returns all available data windows and targets as a single batch.

        Returns:
            _TransformedData with:
                - x of shape (total_windows, window_size, n_features)
                - y of shape (total_windows, n_features)
        """
        # Get all indices
        all_indices = list(range(len(self)))

        # Use __getitem__ to get all data
        if not all_indices:
            n_features = self.data.shape[1]
            # Return empty arrays/tensors with correct shapes if no data
            empty_x = np.zeros(
                (0, self.window_size, n_features), dtype=self.data.dtype)
            empty_y = np.zeros((0, n_features), dtype=self.data.dtype)

            if self.tensor_cast:
                empty_x = torch.tensor(
                    empty_x, dtype=self.dtype, device=self.device)
                empty_y = torch.tensor(
                    empty_y, dtype=self.dtype, device=self.device)

            return empty_x, empty_y

        return self[all_indices]


class BiDirectionalTrainer(BaseTrainer):
    '''
    Bi-Directional trainer
    '''

    def __init__(
        self,
        data: Data,
        plot_engine: PlotEngine,
        preprocess: Preprocess,
        metrics: Metrics,
        models: List[BaseBiDirectionalModel],
        combine_methods: List[BaseCombineMethod],
        batch_size: Optional[int] = None,
        auto_plot: bool = True,
        dtype: Optional[torch.dtype] = None,
        device: Optional[torch.device] = None,
        **kwargs
    ):
        super().__init__(data, plot_engine, preprocess, metrics, models, **kwargs)
        self.combine_methods = combine_methods
        self.batch_size = batch_size or 1
        self.device = device or get_accelerate_device()
        self.dtype = dtype or torch.float32
        self.__auto_plot = auto_plot

        # Cached data
        self.__cached_transformed_data: List[_TransformedData] = None
        self.__cached_transformed_data_generator: List[DataTransformer] = None
        self.result = None

    def __transforming_data(
        self,
        use_generator: bool = False,
        tensor_cast: bool = False
    ) -> List[Union[_TransformedData, DataTransformer]]:
        '''
        Transforming data for training models. If use_generator is True, return generator object.

        Transforming shapes:
            Original: (n_samples, n_features)
            Transformed:
                - x: (n, window_size, n_features)
                - y: (n, n_features)
        > `n` is the number data from the missing position to the most left or right position, \
            or the number of batches if use_generator is True.

        Returns:
            List of transformed data or generator object
        '''
        # 1. Get from cache
        if use_generator:
            if self.__cached_transformed_data_generator is not None:
                return self.__cached_transformed_data_generator
        else:
            if self.__cached_transformed_data is not None:
                return self.__cached_transformed_data

        # 2. Initialize variables
        data_list = []

        # 3. Iterate over missing positions
        for position in self.data.missing_positions.values():
            _most_left_pos = min([pos[0] for pos in position])
            _most_right_pos = max([pos[1] for pos in position])

            # 2. Get position of not missing data
            _data_begin_to_left = self.data.dataframe.iloc[:_most_left_pos].to_numpy(
            )
            _data_right_to_end = self.data.dataframe.iloc[_most_right_pos:].to_numpy(
            )
            _data_right_to_end = np.flip(_data_right_to_end, axis=0)

            # 3. Generate data pairs
            _data_left = DataTransformer(
                data=_data_begin_to_left,
                window_size=self.data.window_size,
                batch_size=self.batch_size,
                device=self.device,
                dtype=self.dtype,
                tensor_cast=tensor_cast
            )
            _data_right = DataTransformer(
                data=_data_right_to_end,
                window_size=self.data.window_size,
                batch_size=self.batch_size,
                device=self.device,
                dtype=self.dtype,
                tensor_cast=tensor_cast
            )

            # 3.1. If not use generator, append to list
            if not use_generator:
                _data_left = _data_left()
                _data_right = _data_right()

            # 4. Append to list
            data_list.append(_data_left)
            data_list.append(_data_right)

        # 5. Cache data
        if use_generator:
            self.__cached_transformed_data_generator = data_list
        else:
            self.__cached_transformed_data = data_list

        return data_list

    def __get_last_window_by_position(
        self,
        postion: int,
        use_backward_window: bool = False,
        tensor_cast: bool = False
    ) -> _TensorType:
        '''
        Get the last window for forecasting by missing position
        Returns:
            Last window data of shape (window_size, n_features)
        '''
        _last_window = []
        for col in self.data.dataframe.columns:
            if use_backward_window:
                _pos = self.data.missing_positions[col][postion][1]
                _last_window.append(np.flip(
                    self.data.dataframe[col].iloc[_pos:_pos + self.data.window_size].to_numpy(), axis=0
                ))
            else:
                _pos = self.data.missing_positions[col][postion][0]
                _last_window.append(
                    self.data.dataframe[col].iloc[_pos - self.data.window_size:_pos].to_numpy())

        if tensor_cast:
            return torch.tensor(np.array(_last_window).T, device=self.device, dtype=self.dtype)
        return np.array(_last_window).T

    def __plot_result(
        self,
        x: npt.ArrayLike,
        y: npt.ArrayLike,
        labels: List[str],
        missing_idx: str,
        model_name: Optional[str] = None,
        combine_method: Optional[str] = None
    ):
        data = np.stack(
            (x, y), axis=0)
        split_data = np.split(
            data, self.data.n_features, axis=2)
        split_data = [np.squeeze(
            t, axis=2).T for t in split_data]
        paths = []
        for i, data in enumerate(split_data):
            n = f"{' vs '.join(labels)} on {self.data.name} ({self.data.dataframe.columns[i]}, {missing_idx})"
            if model_name:
                n += f" using {model_name}"
            if combine_method:
                n += f" with {combine_method}"
            path = self.plot_engine.from_numpy(
                data=data,
                labels=labels,
                name=n,
            )
            paths.append(path)
        return paths

    def __plot_history(
        self,
        history: list[float],
        model_name: str,
        missing_idx: str,
        direction: str
    ):
        n = f"Loss history of {model_name} on {self.data.name} ({missing_idx}) in {direction} direction"
        path = self.plot_engine.from_numpy(
            data=np.array(history).reshape(-1, 1),
            labels=["Loss"],
            name=n
        )
        return path

    def train(self):
        '''
        Train models with given experiment configuration
        '''
        # 1. Initialization
        train_results: List[TrainResult] = []

        # 2. Iterate over models & Generate sliding window data
        for model in self.models:
            summary_info = model.summary()
            if summary_info:
                _train_verbose(summary_info)

            # 2.1 If model want to use generator object
            data_list = self.__transforming_data(
                use_generator=model.use_generator,
                tensor_cast=model.use_tensor_cast
            )

            # 3. Iterate over data
            num_results_count = 0
            current_missing_position = 0
            forecasted_data = []
            train_time = 0
            infer_time = 0

            # 3.1. Iterate over data list
            for _data in data_list:
                use_backward_window = num_results_count % 2 == 1

                # 4. Train model
                _train_t_s = time.perf_counter()
                _train_verbose(
                    f"Training {model.name}, position {current_missing_position}, {'backward' if use_backward_window else 'forward'} direction")
                if model.use_generator:
                    model.train(_data, None)
                else:
                    model.train(*_data)
                train_time += time.perf_counter() - _train_t_s

                # 5. Get data for forecasting
                x_data = self.__get_last_window_by_position(
                    current_missing_position,
                    use_backward_window=use_backward_window,
                    tensor_cast=model.use_tensor_cast
                )  # (window_size, n_features)

                # 5.1. Forecast by number of missing (gap_size)
                _infer_t_s = time.perf_counter()
                for _ in log.progress(range(self.data.gap_size), desc=f"Forecasting {'backward' if use_backward_window else 'forward'}"):
                    y_pred = model.forecast(x_data)

                    # 5.2. Reshape y_pred if needed
                    if len(y_pred.shape) == 1:
                        y_pred = y_pred.reshape(1, -1)

                    # 5.3. Update x_data
                    if model.use_tensor_cast:
                        x_data = torch.cat([x_data[1:], y_pred])
                    else:
                        x_data = np.concatenate([x_data[1:], y_pred])
                infer_time += time.perf_counter() - _infer_t_s

                # 5.4. Reverse data if using backward window
                if use_backward_window:
                    if model.use_tensor_cast:
                        x_data = torch.flip(x_data, [0])
                    else:
                        x_data = np.flip(x_data, axis=0)

                # 5.5. Append to forecasted data
                if model.use_tensor_cast:
                    forecasted_data.append(x_data.detach().cpu().numpy())
                else:
                    forecasted_data.append(x_data)

                # 5.6. Reset model if needed
                if not model.continuously:
                    model.reset()

                # 5.7. Update flags
                num_results_count += 1

                # 6. If number of results is even, update missing position, perform combine result
                if num_results_count % 2 == 0:
                    # 6.1. Get actual data
                    y_true = self.data.get_actual_from_missing_index(
                        current_missing_position)

                    # 6.2. Combine results
                    for combine_method in self.combine_methods:
                        final_y_pred = combine_method.combine(
                            forward=forecasted_data[0],
                            backward=forecasted_data[1],
                            current_missing_index=current_missing_position
                        )

                        # 6.3. Reverse processing data if needed
                        final_y_pred = self.preprocess.reverse_from_numpy(
                            final_y_pred)

                        # 7. Perform metrics calculation
                        result = self.metrics.evaluate(
                            y_true,
                            final_y_pred,
                            model.name,
                            combine_method.__class__.__name__
                        )

                        # 8. Append result
                        train_results.append(TrainResult(
                            names=[model.name, current_missing_position,
                                   combine_method.__class__.__name__],
                            result=final_y_pred,
                            train_time=combine_method.calculate_train_time(train_time),
                            infer_time=combine_method.calculate_infer_time(infer_time),
                            metrics=result,
                            traces={
                                "true": y_true,
                                "forward": self.preprocess.reverse_from_numpy(forecasted_data[0]),
                                "backward": self.preprocess.reverse_from_numpy(forecasted_data[1])
                            }
                        ))

                    # 9. Reset flags
                    current_missing_position += 1
                    forecasted_data = []
                    train_time = 0
                    infer_time = 0

                # 9.1. If model is dynamic, update model index
                if "dynamic" in model.name.lower():
                    model.increment_model_index()

                # 9.2. If model has get_history method, plot history
                if hasattr(model, "get_history"):
                    history = model.get_history()
                    if history:
                        self.__plot_history(
                            history,
                            model.name,
                            current_missing_position,
                            "backward" if use_backward_window else "forward"
                        )

        # 10. Plot results
        if self.__auto_plot:
            for result in train_results:
                # 10.1. Plot actual vs predicted
                self.__plot_result(
                    result["traces"]["true"],
                    result["result"],
                    ["Actual", "Predicted"],
                    result["names"][1],
                    result["names"][0],
                    result["names"][2]
                )

                # 10.2. Plot actual vs forward
                self.__plot_result(
                    result["traces"]["true"],
                    result["traces"]["forward"],
                    ["Actual", "Forward"],
                    result["names"][1],
                    result["names"][0],
                    result["names"][2]
                )

                # 10.3. Plot actual vs backward
                self.__plot_result(
                    result["traces"]["true"],
                    result["traces"]["backward"],
                    ["Actual", "Backward"],
                    result["names"][1],
                    result["names"][0],
                    result["names"][2]
                )

        # 11. Return results
        _train_verbose("🎉 Training completed")
        self.result = train_results
        return self.result
