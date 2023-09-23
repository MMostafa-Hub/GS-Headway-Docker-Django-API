from unittest import TestCase, mock

import pandas as pd

from ..timeseries.configuration_manager import ConfigurationManager
from ..timeseries.timeseries_simulator import TimeSeriesParams


class TestConfigurationManager(TestCase, ConfigurationManager):
    def setUp(self) -> None:
        self.perfect_config_data = {
            "time_index": {
                "start_date": "2019-01-01",
                "end_date": "2023-01-01",
                "sampling_frequency_in_minutes": 60,  # 1 hour
            },
            "multiplicative": True,
            "main_components": {
                "trend": {
                    "coefficients": [0.005, 0.001],
                },
                # You can add more than one seasonality component
                "seasonality": [
                    {"in_days": False, "period": 24, "amplitude": 0.5},  # Daily
                    {"in_days": True, "period": 365, "amplitude": 0.005},  # Yearly
                ],
            },
            "residual_components": {
                "noise": {"noise_level": 0.1},
                "outliers": {"outlier_ratio": 0.001},
            },
        }

    def test_public_params_missing_keys(self):
        """Tests that the __params method raises a KeyError when the configuration dictionary is missing keys."""
        incomplete_config_data = {
            "time_index": {
                "start_date": "2019-01-01",
                "end_date": "2023-01-01",
                "sampling_frequency_in_minutes": 60,  # 1 hour
            },
            "multiplicative": True,
            # Missing main_components
        }
        with self.assertRaises(KeyError):
            self._params(incomplete_config_data)

    def test__params_success(self):
        import pandas as pd

        config = self.perfect_config_data
        time_series_params = self._params(config)
        # Testing the type of the returned object
        self.assertIsInstance(time_series_params, TimeSeriesParams)

        # Testing the time index
        self.assertEqual(
            list(time_series_params.time_index),
            list(pd.date_range(start="2019-01-01", end="2023-01-01", freq="60T")),
        )

        # Testing the multiplicative flag
        self.assertTrue(time_series_params.multiplicative)

        # Testing the main components
        self.assertEqual(len(time_series_params.main_components), 3)
        self.assertEqual(
            time_series_params.main_components[0].coefficients, [0.005, 0.001]
        )
        self.assertEqual(time_series_params.main_components[1].period, 24)
        self.assertEqual(time_series_params.main_components[2].period, 365)

        # Testing the residual components
        self.assertEqual(len(time_series_params.residual_components), 2)
        self.assertEqual(time_series_params.residual_components[0].noise_level, 0.1)
        self.assertEqual(time_series_params.residual_components[1].outlier_ratio, 0.001)

    def test_public_params_empty_dict(self):
        empty_config_data = {}
        with self.assertRaises(KeyError):
            self._params(empty_config_data)

    def test_public_params_empty_main_components(self):
        config_data = self.perfect_config_data.copy()
        config_data["main_components"] = []
        with self.assertRaises(Exception):
            self._params(config_data)

    def test_public_params_start_date_later_than_end_date(self):
        config_data = self.perfect_config_data.copy()
        config_data["time_index"]["start_date"] = "2023-01-01"
        config_data["time_index"]["end_date"] = "2019-01-01"

        # should return an empty time index
        time_series_params = self._params(config_data)
        self.assertEqual(len(time_series_params.time_index), 0)

    @mock.patch("pandas.date_range")
    def test_public_params_date_range_called_correctly(
        self, mock_date_range: mock.Mock
    ):
        self._params(self.perfect_config_data)
        mock_date_range.assert_called_once_with(
            start=pd.Timestamp("2019-01-01"), end=pd.Timestamp("2023-01-01"), freq="60T"
        )
