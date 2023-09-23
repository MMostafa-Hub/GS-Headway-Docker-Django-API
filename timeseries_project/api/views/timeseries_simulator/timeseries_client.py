from timeseries.configuration_manager import ConfigurationManager
from timeseries.timeseries_producer import TimeSeriesProducer
from timeseries.timeseries_simulator import TimeSeriesSimulator
import sys


def main():
    config_path, config_path_ext, dump_path, dump_path_ext = get_paths()

    # Reading the configuration file
    time_series_params = getattr(ConfigurationManager, config_path_ext)(config_path)

    # Creating the time series generator
    time_series_generator = TimeSeriesSimulator(time_series_params)

    # Generating the time series
    time_series = time_series_generator.simulate()

    # Saving the time series
    getattr(TimeSeriesProducer, dump_path_ext)(dump_path, time_series)


def get_paths():
    cl_args = sys.argv[1:]  # Getting the command line arguments
    config_path = cl_args[0]  # Getting the path to the configuration file
    dump_path = cl_args[1]  # Getting the path to the dump file
    # Extract file extension of config_path
    config_path_ext = config_path.split(".")[-1]
    # Extract file extension of dump_path
    dump_path_ext = dump_path.split(".")[-1]
    return config_path, config_path_ext, dump_path, dump_path_ext


if __name__ == "__main__":
    main()
