# Time Series Simulator REST API

Is a simple and easy-to-use api for generating time series data samples built in Django.

## Features

- Can specify multiple datasets attributes in a single request.
- Check the status of the request.
- Download the generated data.
- Stop the generation process, if it takes too long.
- Restart the generation process, if it fails.
- Save the time series data in the database.
- List all the use cases.
- The ability to extend the program, by only *adding* your custom functions or classes. (See the class diagram)

## Installation

To run the api, you will need Python 3 and the dependencies in the `requirements.txt` file.

## Usage

1. Install any API testing tool like [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/).
2. Install the dependencies in the `requirements.txt` file.
3. Run the server by running the command `python manage.py runserver` in the root directory.
4. Open the API testing tool and create a request to the server.

## Example

### 1. Creating a Use Case

Create a GET request to `api/use_case` with a request body like this:

```JSON
{
  "name": "use_case_1",
  "start_date": "2021-01-01",
  "end_date": "2022-01-01",
  "type": "additive",
  "datasets": [
    {
      "frequency": "1H",
      "trend_coefficients": [
        0.1,
        2.5,
        1,
        3
      ],
      "missing_percentage": 0.06,
      "outlier_percentage": 10,
      "noise_level": 10,
      "cycle_amplitude": 3,
      "cycle_frequency": 1,
      "seasonality_components": [
        {
          "frequency": "Weekly",
          "multiplier": 1,
          "phase_shift": 0,
          "amplitude": 3
        },
        {
          "frequency": "Daily",
          "multiplier": 2,
          "phase_shift": 90,
          "amplitude": 5
        }
      ]
    }
  ]
}
```

### 2. List all the use cases

Create a GET request to `api/list_simulators` with no request body.
The Response should look like this

```JSON
[
  "use_case_1"
]
```

### 3. Stop the generation process

Create a POST request to `api/stop_simulator` with a request body like this:

```JSON
{
  "name": "use_case_1"
}
```

### 4. Restart the generation process

If the generation process fails, you can restart it by creating a POST request to `api/restart_simulator` with a request body like this:

```JSON
{
  "name": "use_case_1"
}
```

### 5. Check the status of the request

Create a GET request to `api/check_status` with a request body like this:

```JSON
{
  "name": "use_case_1"
}
```

And the response should look like this:

```JSON
  "Succeeded"
```

The status of the request can be:

- `Submitted`: The request has been submitted.
- `Succeeded`: The generation process has finished successfully.
- `Failed`: The generation process has failed or stopped.
- `Running`: The generation process is still running.
