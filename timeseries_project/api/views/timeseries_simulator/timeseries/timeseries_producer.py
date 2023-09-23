import pandas as pd
from django.db import models


class TimeSeriesProducer:
    """This class is responsible for writing the time series to any format."""

    @staticmethod
    def csv(path: str, time_series: pd.Series):
        """Writes the time series to a CSV file."""
        time_series.to_csv(path, index=False)

    @staticmethod
    def to_django_model(model: models.Model, identifier, time_series: pd.Series):
        """Writes the time series to a Django model."""
        time_series_json = time_series.to_json(index=False)
        model.objects.filter(id=identifier).update(time_series=time_series_json)
