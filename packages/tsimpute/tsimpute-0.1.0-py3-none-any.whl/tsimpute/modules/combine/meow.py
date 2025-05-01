'''
Mapping Error Onto Weight (MEOW)
'''
import numpy as np
from tsimpute.modules.combine.base import BaseCombineMethod


class MEOW(BaseCombineMethod):
    '''
    Mapping Error Onto Weight (MEOW)
    '''

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.e = kwargs.get("e", 0.1)

    def combine(self, forward, backward, current_missing_index):
        self.shape_validation(forward, backward)

        # 1. Calculate weights
        i = np.arange(forward.shape[0], dtype=np.float32) + 1
        weights = - 1 / forward.shape[0] * i * (1 - 2 * self.e) + (1 - self.e)

        # 2. Expand weights to match the input shape
        weights = weights[:, np.newaxis]

        # 3. Combine using broadcasting
        return forward * weights + backward * (1 - weights)
