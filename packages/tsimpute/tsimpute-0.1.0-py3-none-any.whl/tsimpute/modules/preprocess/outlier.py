'''
Outlier removal module
'''
from tsimpute.modules.preprocess.base import BaseProcess


class OutlierRemoval(BaseProcess):
    def __init__(
        self,
        upper: float = 0.75,
        lower: float = 0.25,
        shift: float = 3.0
    ):
        super().__init__()
        self.upper = upper
        self.lower = lower
        self.shift = shift

    def flow(self, data):
        q1 = data.quantile(self.lower)
        q3 = data.quantile(self.upper)
        iqr = q3 - q1
        outlier = (data < (q1 - self.shift * iqr)
                   ) | (data > (q3 + self.shift * iqr))
        for col in data.columns:
            data.loc[outlier[col], col] = data[col].mean()
        return data
