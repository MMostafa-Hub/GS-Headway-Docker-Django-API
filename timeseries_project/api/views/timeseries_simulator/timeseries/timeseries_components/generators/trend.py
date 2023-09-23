from .generator import Generator
import pandas as pd
import numpy as np
from typing import List


class TrendGenerator(Generator):
    def __init__(self, coefficients: List[float] = (1.0,)) -> None:
        """Initialize the coefficients of the trend component.

        Args:
            coefficients (List[float]): The coefficients of the polynomial, in descending order.
                         For example, [a, b, c] corresponds to a*t^2 + b*t + c.
                         where t is the time index.
        """
        super().__init__()
        self.coefficients = coefficients

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """Generate the trend component for a time series."""
        # sequence of numbers from 0 to the number of timestamps
        time = np.arange(len(time_index))
        return pd.Series(np.polyval(self.coefficients, time))
