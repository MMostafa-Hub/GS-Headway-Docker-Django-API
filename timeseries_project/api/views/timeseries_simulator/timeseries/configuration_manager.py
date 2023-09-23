from typing import Any, List

import pandas as pd
import yaml
from rest_framework import serializers

from .timeseries_simulator import TimeSeriesParams
from .timeseries_components.generators.seasonality import SeasonalityGenerator
from .timeseries_components.generators.trend import TrendGenerator
from .timeseries_components.transformers.noise import NoiseTransformer
from .timeseries_components.transformers.outlier import OutlierTransformer
from .timeseries_components.transformers.missing_value import MissingValueTransformer


class ConfigurationManager:
    @staticmethod
    def _params(use_case: dict[str, Any]) -> List[TimeSeriesParams]:
        """Unpacks the use case and returns a list of time series parameters."""
        start_date = pd.Timestamp(use_case["start_date"])
        end_date = pd.Timestamp(use_case.get("end_date", None))
        data_size = use_case.get("data_size", None)
        multiplicative = use_case["type"] == "multiplicative"
        time_series_param_list = []
        for dataset in use_case["datasets"]:
            frequency = dataset["frequency"]
            # Creating the time index
            if data_size:
                time_index = pd.date_range(
                    start=start_date, periods=data_size, freq=frequency
                )
            else:
                time_index = pd.date_range(
                    start=start_date, end=end_date, freq=frequency
                )

            # Creating the Residual components
            noise_level = dataset["noise_level"]
            outlier_ratio = dataset["outlier_percentage"] / 100
            missing_values_ratio = dataset["missing_percentage"] / 100

            residual_components = [
                NoiseTransformer(noise_level),
                OutlierTransformer(outlier_ratio),
                MissingValueTransformer(missing_values_ratio),
            ]

            # Creating the Main components
            trend_coefficients = dataset["trend_coefficients"]

            cycle_amplitude = dataset["cycle_amplitude"]
            cycle_frequency = dataset["cycle_frequency"]

            main_components = [
                TrendGenerator(trend_coefficients),
                SeasonalityGenerator(
                    period=365,  # Year
                    amplitude=cycle_amplitude,
                    phase_shift=0,
                    in_days=True,
                    multiplier=cycle_frequency,
                ),
            ]
            seasonality_components = dataset["seasonality_components"]
            for seasonality_component in seasonality_components:
                seasonality_type = seasonality_component["frequency"]
                seasonality_amplitude = seasonality_component["amplitude"]
                seasonality_phase_shift = seasonality_component["phase_shift"]
                seasonality_multiplier = seasonality_component["multiplier"]
                seasonality_period = 0
                if seasonality_type == "Daily":
                    seasonality_period = 1
                elif seasonality_type == "Weekly":
                    seasonality_period = 7
                elif seasonality_type == "Monthly":
                    seasonality_period = 30

                main_components.append(
                    SeasonalityGenerator(
                        period=seasonality_period,
                        amplitude=seasonality_amplitude,
                        phase_shift=seasonality_phase_shift,
                        multiplier=seasonality_multiplier,
                        in_days=True,
                    )
                )

            # Creating the time series parameters
            time_series_params = TimeSeriesParams(
                time_index=time_index,
                main_components=main_components,
                residual_components=residual_components,
                multiplicative=multiplicative,
            )
            time_series_param_list.append(time_series_params)

        return time_series_param_list

    @staticmethod
    def yaml(path: str) -> List[TimeSeriesParams]:
        with open(path, "r") as file:
            config_data = file.read()

        config = yaml.load(config_data, Loader=yaml.FullLoader)
        return ConfigurationManager._params(config)

    @staticmethod
    def sqlite_db(serializer: serializers.ModelSerializer) -> List[TimeSeriesParams]:
        use_case = serializer.data
        return ConfigurationManager._params(use_case)
