'''
Scaler module
'''
from typing import Union
from enum import Enum
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tsimpute.modules.preprocess.base import BaseProcess, PreprocessError


class ScalerType(Enum):
    MinMax = "MinMax"
    Standard = "Standard"

    @staticmethod
    def get_by_str(name: str):
        if name == "MinMax":
            return ScalerType.MinMax
        elif name == "Standard":
            return ScalerType.Standard
        else:
            raise PreprocessError("Invalid scaler type")


class Scaler(BaseProcess):
    def __init__(self, scaler_type: Union[ScalerType, str] = None):
        super().__init__()
        self.use_numpy = True

        # Get scaler type
        if isinstance(scaler_type, str):
            self.scaler_type = ScalerType.get_by_str(scaler_type)
        else:
            self.scaler_type = scaler_type or ScalerType.MinMax

        # Initialize scaler
        if self.scaler_type == ScalerType.MinMax:
            self.scaler = MinMaxScaler()
        elif self.scaler_type == ScalerType.Standard:
            self.scaler = StandardScaler()
        else:
            raise PreprocessError(
                f"Invalid scaler type. Must be one of {self.scaler_type}")

    def flow(self, data):
        return self.scaler.fit_transform(data)

    def reverse(self, data):
        return self.scaler.inverse_transform(data)
