from .transformer import Transformer
import pandas as pd
import numpy as np


class NoiseTransformer(Transformer):
    def __init__(self, noise_level: float) -> None:
        super().__init__()
        self.noise_level = noise_level

    def transform(self, time_series: pd.Series) -> pd.Series:
        """Add noise to the time series data."""
        noise = np.random.normal(0, self.noise_level, size=len(time_series))
        return pd.Series(time_series.copy() + noise)
