from rest_framework import serializers
from .models import UseCase, Dataset, SeasonalityComponent


class SeasonalityComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalityComponent
        fields = ["frequency", "multiplier", "phase_shift", "amplitude"]


#
class DatasetSerializer(serializers.ModelSerializer):
    seasonality_components = SeasonalityComponentSerializer(
        many=True
    )  # Dataset has many seasonality components

    class Meta:
        model = Dataset
        fields = [
            "frequency",
            "trend_coefficients",
            "missing_percentage",
            "outlier_percentage",
            "noise_level",
            "cycle_amplitude",
            "cycle_frequency",
            "seasonality_components",
        ]


class UseCaseSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True)  # UseCase has many datasets

    class Meta:
        model = UseCase
        fields = ["name", "start_date", "end_date", "data_size", "type", "datasets"]

    def validate(self, attrs):
        """Checks that either the end date or the data size is provided, but not both."""
        if not (
            bool(attrs.get("end_date", False)) ^ bool(attrs.get("data_size", False))
        ):
            raise serializers.ValidationError(
                "Either the end date or the data size must be provided, but not both."
            )
        return attrs

    def create(self, validated_data):
        """Creates a user case and its associated datasets and seasonality components."""
        datasets_data = validated_data.pop(
            "datasets"
        )  # Remove the datasets data from the validated data

        use_case = UseCase.objects.create(**validated_data)  # Create the use case

        # Create the datasets and associate them with the use_case
        for dataset_data in datasets_data:
            seasonality_components_data = dataset_data.pop(
                "seasonality_components"
            )  # Remove the seasonality components data from the dataset

            # Create the dataset and associate it with the use_case
            dataset = Dataset.objects.create(**dataset_data, use_case=use_case)

            # Create the seasonality components and associate them with the dataset
            for seasonality_component_data in seasonality_components_data:
                seasonality_component = SeasonalityComponent.objects.create(
                    **seasonality_component_data,
                    dataset=dataset  # Associate the seasonality component with the dataset
                )

        return use_case
