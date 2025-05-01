'''
Plot engine for visualize data
'''
from typing import Callable, Union, Dict, Optional, Tuple, List
import os
from PIL import Image
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from tsimpute.core.utils import slugnify


_OnSaveCallback = Callable[[Image.Image, str], None]


_DEFAULT_DIR = os.path.join(os.getcwd(), 'output')
_DEFAULT_STYLE = 'seaborn-v0_8'
_DEFAULT_CMAP = 'viridis'


class PlotEngine:
    '''
    Plot engine for visualize data

    Parameters
    ----------
    plot_style: str
        Matplotlib style
    cmap: str
        Colormap
    directory: str
        Directory to save plots
    num_cols: int
        Number of columns in the plot
    root_size: Tuple[int, int]
        Root size of the plot
    on_save_callback: Callable[[Image.Image, str], None]
        Callback function when saving the plot
    '''

    def __init__(
        self,
        plot_style: Optional[str] = None,
        cmap: Optional[str] = None,
        directory: Optional[str] = None,
        num_cols: Optional[int] = None,
        root_size: Optional[Tuple[int, int]] = None,
        on_save_callback: Optional[_OnSaveCallback] = None
    ):
        # Set configuration
        self.__plot_style = plot_style or _DEFAULT_STYLE
        self.__cmap = mpl.colormaps.get_cmap(cmap or _DEFAULT_CMAP)
        self.__directory = directory or _DEFAULT_DIR
        self.__num_cols = num_cols or 1
        self.__root_size = root_size or (10, 3)
        self.__on_save: _OnSaveCallback = on_save_callback

        # Set matplotlib style
        plt.style.use(self.__plot_style)

    def set_directory(self, directory: str):
        self.__directory = directory

    def set_on_save(self, on_save: _OnSaveCallback):
        self.__on_save = on_save

    def from_dataframe(
        self,
        dataframe: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
        name: Optional[str] = None
    ) -> str:
        # 1. Check if dataframe is a DataFrame
        if isinstance(dataframe, pd.DataFrame):
            _dataframe: Dict[str, pd.Series] = {
                _k: _s for _k, _s in dataframe.items()}
        else:
            _dataframe: Dict[str, pd.Series] = {}
            for name, df in dataframe.items():
                for _k, _s in df.items():
                    _dataframe[f"{name.capitalize()} - {_k}"] = _s

        # 2. Validate directory, and valid num cols
        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)
        if len(_dataframe) < self.__num_cols:
            self.__num_cols = len(_dataframe)

        # 3. Calculate rows and columns
        nrows = (len(_dataframe) + self.__num_cols - 1) // self.__num_cols
        ncols = min(self.__num_cols, len(_dataframe))

        # 4. Create subplots
        fig, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(
                self.__root_size[0] * ncols,
                self.__root_size[1] * nrows
            )
        )
        axes = np.array(axes).flatten()

        # 5. Plot data
        _colors = self.__cmap(np.linspace(0, 1, len(_dataframe)))
        for idx, (key, df) in enumerate(_dataframe.items()):
            if idx < len(axes):
                ax = axes[idx]
                ax.plot(df, color=_colors[idx])
                ax.set_title(key)
                ax.set_xlabel('Time')
                ax.set_ylabel('Value')

                # 5.1. Set xticks
                if pd.api.types.is_datetime64_any_dtype(df.index):
                    # Automatically choose tick intervals
                    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                    ax.xaxis.set_major_formatter(
                        mdates.DateFormatter('%Y-%m-%d'))
                else:
                    # For numeric indices, use the dynamic tick spacing above
                    if len(df) > 20:
                        step = max(1, len(df) // 10)
                        ax.set_xticks(np.arange(0, len(df), step))
                    else:
                        ax.set_xticks(np.arange(0, len(df), 1))

        # 5.2. Set title and layout
        fig.tight_layout()

        # 6. Save figure
        path = os.path.join(
            self.__directory, f"{slugnify(name or 'Plot')}.jpg")
        fig.savefig(path)
        if self.__on_save:
            fig.canvas.draw()
            _buffer = fig.canvas.buffer_rgba()
            _img = Image.frombytes(
                'RGBA', fig.canvas.get_width_height(), _buffer).convert('RGB')
            self.__on_save(_img, path)
        plt.close(fig)
        return path

    def from_numpy(
        self,
        data: np.ndarray,
        labels: Optional[Union[str, List[str]]] = None,
        name: Optional[str] = None
    ) -> str:
        # 1. Validate input
        if not isinstance(data, np.ndarray):
            raise ValueError("data must be a numpy array")

        if data.ndim != 2:
            raise ValueError("data must be a 2D numpy array")

        num_features = data.shape[1]

        if labels is None:
            labels = [f"Feature {i+1}" for i in range(num_features)]
        elif isinstance(labels, str):
            raise ValueError(
                "labels must be a list or tuple matching the number of features")
        elif len(labels) != num_features:
            raise ValueError(
                f"labels must contain exactly {num_features} elements for {num_features} features")

        # 2. Validate directory
        if not os.path.exists(self.__directory):
            os.makedirs(self.__directory)

        # 3. Create subplots
        fig, ax = plt.subplots(figsize=self.__root_size)

        # 4. Plot data
        ax.plot(data, label=labels)
        ax.set_title(name or 'Plot')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend()

        # 5. Save figure
        path = os.path.join(
            self.__directory, f"{slugnify(name or 'Plot')}.jpg")
        fig.savefig(path)

        if self.__on_save:
            fig.canvas.draw()
            _buffer = fig.canvas.buffer_rgba()
            _img = Image.frombytes(
                'RGBA', fig.canvas.get_width_height(), _buffer).convert('RGB')
            self.__on_save(_img, path)

        plt.close(fig)
        return path
