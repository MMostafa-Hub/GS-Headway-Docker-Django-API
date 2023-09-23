from abc import ABC, abstractmethod
import pandas as pd


class Generator(ABC):
    @abstractmethod
    def generate(self, time_index: pd.DatetimeIndex) -> pd.Series:
        """Generates the time series component."""
        pass
