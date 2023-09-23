from .transformer import Transformer
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple


class NormalizationTransformer(Transformer):
    def __init__(self, feature_range: Tuple[int, int]) -> None:
        super().__init__()
        self.feature_range = feature_range

    def transform(self, time_series: pd.Series) -> pd.Series:
        """Normalize the time series data by subtracting the mean and dividing by the standard deviation.
        Which is implemented by the MinMaxScaler in sklearn.
        """

        scaler = MinMaxScaler(feature_range=self.feature_range)
        values = time_series.values
        values = np.array(values).reshape(-1, 1)
        return pd.Series(scaler.fit_transform(values))
