import pandas as pd
from typing import List
from .timeseries_components.transformers.transformer import Transformer
from .timeseries_components.generators.generator import Generator
from operator import mul, add
from functools import reduce
from dataclasses import dataclass


@dataclass
class TimeSeriesParams:
    time_index: pd.DatetimeIndex
    main_components: List[Generator]
    residual_components: List[Transformer]
    multiplicative: bool = True


class TimeSeriesSimulator:
    def __init__(
        self,
        time_series_params: TimeSeriesParams,
    ) -> None:
        """Initialize the time series generator."""
        self.time_index = time_series_params.time_index
        self.multiplicative = time_series_params.multiplicative
        self.main_components = time_series_params.main_components
        self.residual_components = time_series_params.residual_components

    def simulate(self) -> pd.Series:
        """Generates a time series based on the main and residual components."""
        # Choosing the operation to be performed based on the time series type
        operation = mul if self.multiplicative else add

        # Applying the main components
        result_series = pd.Series(
            reduce(
                lambda x, y: operation(x, y),
                [mc.generate(self.time_index) for mc in self.main_components],
            )
        )

        # Applying the residual components
        for rc in self.residual_components:
            result_series = rc.transform(result_series)

        return result_series
