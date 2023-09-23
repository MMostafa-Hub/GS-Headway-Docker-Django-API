import threading
import time

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from ..serializers import UseCaseSerializer
from ..models import UseCase, Dataset
from .timeseries_simulator.timeseries.configuration_manager import ConfigurationManager
from .timeseries_simulator.timeseries.timeseries_producer import TimeSeriesProducer
from .timeseries_simulator.timeseries.timeseries_simulator import TimeSeriesSimulator


def run_simulator(request, serializer):
    """Runs the simulator and saves the results to the database."""
    dataset_ids = UseCase.objects.get(name=request.data["name"]).datasets.values_list(
        "id", flat=True
    )  # Get the dataset IDs associated with the use case
    use_case = UseCase.objects.get(name=request.data["name"])  # Get the use case

    # Get the time series parameters from the database
    time_series_param_list = ConfigurationManager.sqlite_db(serializer)
    for time_series_params, dataset_id in zip(time_series_param_list, dataset_ids):
        time_series_simulator = TimeSeriesSimulator(time_series_params)
        result_time_series = time_series_simulator.simulate()

        # Check the use case again to see if it has been stopped by stop_simulator view
        use_case = UseCase.objects.get(name=request.data["name"])  # Get the use case
        if use_case.flag:
            return

        # Save the time series to output folder and to the database
        TimeSeriesProducer.to_django_model(Dataset, dataset_id, result_time_series)
        TimeSeriesProducer.csv(f"./simulation_output/{use_case.name}_{dataset_id}.csv", result_time_series)

    use_case.status = "Succeeded"
    use_case.flag = False
    use_case.save()


@api_view(["POST"])
def add_use_case(request: Request) -> Response:
    """Adds a use case to the database, and starts a new thread to run the simulator."""
    serializer = UseCaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()  # Save the use case to the database

    # Start a new thread to run the simulator, and associate it with the name of the use case
    simulator_thread = threading.Thread(
        target=run_simulator, args=(request, serializer)
    )

    # Update the status of the use case to "Running"
    use_case = UseCase.objects.get(name=request.data["name"])
    use_case.status = "Running"
    use_case.save()

    # Start the simulator thread
    simulator_thread.start()

    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_simulators(request: Request) -> Response:
    """Returns the names of the simulators that are available."""
    use_cases_simulator_names = UseCase.objects.values_list("name", flat=True)
    return Response(data=use_cases_simulator_names, status=status.HTTP_200_OK)


@api_view(["POST"])
def restart_simulator(request: Request) -> Response:
    """Restarts the simulator thread, by starting a new thread and setting the stop flag to False."""
    request_data_simulator_name = request.data["name"]
    use_case = UseCase.objects.get(name=request_data_simulator_name)
    use_case.status = "Running"

    serializer = UseCaseSerializer(use_case)
    # Start a new thread for the simulator
    simulator_thread = threading.Thread(
        target=run_simulator, args=(request, serializer)
    )
    use_case.flag = False  # Set the stop flag to False
    use_case.save()

    # Start the simulator thread
    simulator_thread.start()

    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def stop_simulator(request: Request) -> Response:
    """Stops the simulator thread, by setting the stop flag to True."""
    request_data_simulator_name = request.data["name"]

    # Check if there's a simulator with this name
    try:
        use_case = UseCase.objects.get(name=request_data_simulator_name)
    except:
        return Response(
            data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the simulator is running
    if use_case.status != "Running":
        return Response(
            data="The simulator has finished", status=status.HTTP_400_BAD_REQUEST
        )

    # Stop the simulator
    use_case.status = "Failed"
    use_case.flag = True
    use_case.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def check_status(request: Request) -> Response:
    """Checks the status of the simulator."""
    request_data_simulator_name = request.data["name"]

    # Check if there's a simulator with this name
    try:
        use_case = UseCase.objects.get(name=request_data_simulator_name)
    except:
        return Response(
            data="This simulator doesn't exist", status=status.HTTP_400_BAD_REQUEST
        )

    return Response(data=use_case.status, status=status.HTTP_200_OK)
