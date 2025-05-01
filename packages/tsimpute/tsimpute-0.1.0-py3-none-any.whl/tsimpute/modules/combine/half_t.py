'''
Half-T Method
'''
import numpy as np
from tsimpute.modules.combine.base import BaseCombineMethod


class HalfT(BaseCombineMethod):
    '''
    Half-T Method.
    Get $alpha$ from the left and $1 - alpha$ from the right. Not weighted.
    '''
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.use_alpha = kwargs.get("use_alpha", False)
        self.alpha = kwargs.get("alpha", 0.5)

    def __gdlfmi(self, idx: int) -> list[tuple[int, int]]:
        '''
        Get data lengths from missing index
        '''
        data_lengths = []
        for col in self.data.dataframe.columns:
            total_length = len(self.data.dataframe[col])
            length_from_left = self.data.missing_positions[col][idx][0]
            length_from_right = total_length - \
                self.data.missing_positions[col][idx][1]
            data_lengths.append(
                (length_from_left, length_from_right))
        return data_lengths

    def combine(self, forward, backward, current_missing_index):
        self.shape_validation(forward, backward)

        # 1. Calculate weights based on the second axis (assuming method returns data for axis 1)
        if self.use_alpha:
            weights = [length[0] / (length[0] + length[1]) for length in self.__gdlfmi(current_missing_index)]
            alpha = np.mean(weights)
        else:
            alpha = self.alpha

        # 2. Determine split points
        left_size = int(alpha * forward.shape[0])
        right_size = int((1 - alpha) * backward.shape[0])
        
        # 3. Extract required portions
        combined = np.vstack((forward[:left_size], backward[-right_size:]))
        return combined

    def calculate_infer_time(self, infer_time):
        return infer_time / 2