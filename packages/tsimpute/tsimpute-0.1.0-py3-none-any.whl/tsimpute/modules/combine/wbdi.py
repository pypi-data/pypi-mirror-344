'''
Weighted Bi-Directional Imputation
'''
import numpy as np
from tsimpute.modules.combine.base import BaseCombineMethod


class WBDI(BaseCombineMethod):
    '''
    Weighted Bi-Directional Imputation (WBDI)
    '''

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
        weights = [length[0] / (length[0] + length[1])
                   for length in self.__gdlfmi(current_missing_index)]

        # 2. Convert to NumPy array and reshape for broadcasting over second axis
        weights_array = np.array(weights, dtype=np.float32)
        weights_array = weights_array[:, np.newaxis]

        # 3. Combine
        return forward * weights_array + backward * (1 - weights_array)
