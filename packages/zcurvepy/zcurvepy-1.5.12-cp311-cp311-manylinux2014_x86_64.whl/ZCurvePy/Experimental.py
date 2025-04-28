import math
import numpy as np
from typing import List

CONSTANT = 1000

class ExperimentalSegmenter:
    def __init__(
        self,
        input_array: np.ndarray,
        halting: int
    ):
        self.input_array = input_array
        self.halting = halting
        self.seg_points: List[int] = []
    
    def _recursion(
        self,
        offset,
        value_array: np.ndarray
    ):
        length = value_array.shape[0]
        k = (value_array[-1] - value_array[0]) / (length - 1)
        fitted_array = value_array - k * np.arange(length) - value_array[0]
        abs_array = np.abs(fitted_array)
        max_index = np.argmax(abs_array)
        measure = abs_array[max_index] * math.log(length) / CONSTANT
        if measure > self.halting:
            self.seg_points.append(offset + max_index)
            left_array = fitted_array[:max_index]
            right_array = fitted_array[max_index:]
            self._recursion(offset, left_array)
            self._recursion(offset + max_index, right_array)
    
    def run(self):
        self._recursion(0, self.input_array)
        return self.seg_points

