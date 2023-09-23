from .generator import Generator
import pandas as pd
import numpy as np


class StaticSignalGenerator(Generator):
    def __init__(self, magnitude: float) -> None:
        """Initialize the magnitude of the static signal component."""
        super().__init__()
        self.magnitude = magnitude

    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """Generate static signal component to a time series."""
        return pd.Series(
            np.ones(time_index.shape[0]) * self.magnitude, index=time_index
        )
