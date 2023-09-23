from abc import ABC, abstractmethod
import pandas as pd


class Transformer(ABC):
    @abstractmethod
    def transform(self, time_series: pd.Series) -> pd.Series:
        pass
