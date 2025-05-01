import numpy as np
from tsimpute.modules.combine.base import BaseCombineMethod


class MeanCombine(BaseCombineMethod):
    '''
    Mean combination method
    '''

    def combine(self, forward, backward, current_missing_index):
        self.shape_validation(forward, backward)
        return np.mean([forward, backward], axis=0)
