'''
Base model for all models
'''
from abc import ABCMeta, abstractmethod
from typing import Union, Generator, Tuple, Any
import numpy.typing as npt
import inspect
import numpy as np
import torch
from tsimpute.core.logger import log, Color
from tsimpute.core.utils import GLOBAL_PROPERTIES, get_accelerate_device


def _model_verbose(msg: str):
    '''
    Print verbose message for model process
    '''
    log.debug(f"{Color.bold}[Model]{Color.reset} {msg}")


_TensorType = Union[npt.NDArray[np.float32], torch.Tensor]


class BaseModel(metaclass=ABCMeta):
    '''
    Base model for all models
    '''
    trainer = "modules.trainer.base.BaseTrainer"
    name = "Model"
    use_generator = False
    use_tensor_cast = False

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.device = get_accelerate_device()
        self.continuously = False

    def set_continuous(self, continuously: bool):
        '''
        Set continuous mode
        '''
        self.continuously = continuously

    def set_device(self, device: Any):
        '''
        Set device for model
        '''
        self.device = device

    def get_property(self, ref: str, kwargs_ref: dict = {}):
        """
        Find the first variable in the current scope that is an instance of the specified class
        and return the requested property value from it.

        Args:
            ref (str): A string in the format "ClassName.property_name" specifying what to find

        Returns:
            Any: The property value from the first matching instance, or the instance itself
                if no property is specified or the property doesn't exist
        """

        # Get class and property names from the ref string
        class_name, property_name = ref.split('.')

        # Prefer get from kwargs
        if property_name in kwargs_ref:
            v = kwargs_ref[property_name]
            del kwargs_ref[property_name]
            return v

        # Get the calling frame to find variables in the caller's scope
        object_data = GLOBAL_PROPERTIES.get(class_name, None)
        if object_data:
            if hasattr(object_data, property_name):
                return getattr(object_data, property_name)
            else:
                return None
        else:
            return None

    @abstractmethod
    def train(
        self,
        x: Union[_TensorType, Generator[Tuple[_TensorType, _TensorType], None, None]],
        y: Union[_TensorType, None]
    ) -> None:
        '''
        x: input data
            shape of data is (n_sample, window_size, n_features)
        y: label data
            shape of data is (n_sample, n_features)
        '''

    @abstractmethod
    def forecast(self, x: _TensorType) -> _TensorType:
        '''
        x: input data
            shape of data is (n_sample, window_size, n_features)
        return: forecasted data
            shape of data is (n_sample, n_features)
        '''

    def reset(self):
        '''
        Reset weights of the model
        '''
        log.warning(
            f"If you see this warning, your {self.name} model does not implement reset method!")

    def summary(self) -> Union[str, None]:
        '''
        Return model summary or None if not available
        '''
        return f'If you see this message, your {self.name} model does not implement summary method!'

    def save(self, path: str) -> None:
        '''
        Save model to given path
        '''
        _model_verbose(f"Saving model to {path}")
        raise NotImplementedError


# ------------------ Bi-Directional Model ------------------ #

_BiDirectionalTrainInput = Union[_TensorType,
                                 Generator[Tuple[_TensorType, _TensorType], None, None]]
_BiDirectionalTrainLabel = Union[_TensorType, None]
_BiDirectionalForecastInput = _TensorType
_BiDirectionalForecastOutput = _TensorType


class BaseBiDirectionalModel(BaseModel):
    '''
    Base model for all bi-directional models
    '''
    trainer = "bidirectional"
    name = "Bi-Directional Model"
    use_generator = False
    use_tensor_cast = False

    @abstractmethod
    def train(self, x: _BiDirectionalTrainInput,
              y: _BiDirectionalTrainLabel) -> None:
        '''
        x: input data
            If use_generator is False: shape of data is (n_sample, window_size, n_features)
            If use_generator is True: generator of (batch_size, window_size, n_features), (batch_size, n_features)
        y: label data
            If use_generator is False: shape of data is (n_sample, n_features)
            If use_generator is True: None
        '''
        raise NotImplementedError

    @abstractmethod
    def forecast(
            self, x: _BiDirectionalForecastInput) -> _BiDirectionalForecastOutput:
        '''
        x: input data
            shape of data is (window_size, n_features)
        return: forecasted data
            shape of data is (1, n_features)
        '''
        raise NotImplementedError


# ------------------ Inpaint Model ------------------ #


class BaseInpaintModel(metaclass=ABCMeta):
    '''
    Base model for all inpaint models
    '''
    name = "Inpaint Model"
    use_generator = False
    use_tensor_cast = False

    @abstractmethod
    def train(self, x: _TensorType, y: _TensorType) -> None:
        '''
        x: input data
            shape of data is (n_sample, window_size, n_features)
        y: label data
            shape of data is (n_sample, window_size, n_features)
        '''

    @abstractmethod
    def forecast(self, x: _TensorType) -> _TensorType:
        '''
        x: input data
            shape of data is (n_sample, window_size, n_features)
        return: forecasted data
            shape of data is (n_sample, window_size, n_features)
        '''
