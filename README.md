# Stormworkspy

Stormworkspy is a lightweight Python library that exposes a simple Flask-based HTTP API for controlling in-game vehicles in *Stormworks: Build and Rescue*. It provides 32 numeric and 32 boolean channels for input and output, making it easy to interact with vehicles programmatically.

## Features

- Background Flask server with a single endpoint `/`
- 32 numeric (`num1`-`num32`) and 32 boolean (`bool1`-`bool32`) parameters
- Updates internal arrays from GET parameters and returns JSON with output states
- Runs the server in a background thread for easy integration in existing scripts
- Sensors use Stormworks 1-based channel numbers for registration

## Repository Structure

```
Stormworkspy/
├── LICENSE              # MIT license information
├── README.md            # Project documentation
├── setup.py             # Packaging script
└── Stormworkspy/        # Python package
    ├── __init__.py      # Package version and exports
    └── Stormworkspy.py  # Implementation of the Stormworkspy class
```

## Installation

Stormworkspy requires **Python 3.6+** and [Flask](https://pypi.org/project/Flask/). Install the package directly from this repository:

```bash
pip install git+https://github.com/DevShaks/Stormworkspy.git
```

Or clone the repository and install locally:

```bash
git clone https://github.com/DevShaks/Stormworkspy.git
cd Stormworkspy
pip install .
```

## Quick Start

Below is a minimal example that starts the API and modifies output values.

```python
from Stormworkspy import Stormworkspy

sw = Stormworkspy()
sw.outnums[0] = 1.23
sw.outbools[0] = True
sw.run_api(host="0.0.0.0", port=5000)

# The API is now running in the background. Access:
#   http://localhost:5000/?num1=42&bool1=true
```

The API will read `num1` and `bool1` from the query parameters, update the internal input arrays, and return a JSON payload containing all 64 output fields.
For a complete example demonstrating sensor registration, see [`examples/distance.py`](examples/distance.py).

## Running Tests

To run the library's unit tests use the built in test discovery:

```bash
python -m unittest discover tests
```

### Named channels

You can register human friendly names for the numeric and boolean channels. Once
registered, attributes transparently read from or write to the underlying
arrays:

```python
sw = Stormworkspy()
sw.set_num_output("oMotor")  # uses the next free numeric output slot (index 0)
sw.oMotor = 11               # equivalent to sw.outnums[0] = 11
```


### Sensors


Sensors encapsulate logic for reading values from the input channels. Register a
sensor with `register_sensor` and it becomes available as an attribute with IDE
autocompletion. Channels are registered using 1-based channel numbers (e.g.
`channel_distance=1` corresponds to `num1`):

```python
from Stormworkspy.sensors import SW_LaserDistanceSensor

sw = Stormworkspy()
sw.register_sensor("distance", SW_LaserDistanceSensor, channel_distance=2)

print(sw.distance.get_distance())
```
## Contributing

Contributions and bug reports are welcome. Please open an issue or submit a pull request on GitHub. Be sure to include tests and follow the existing code style where possible.

## Disclaimer

See [Disclaimer.md](Disclaimer.md) for information about this project's relationship with Stormworks: Build and Rescue.

## License

This project is released under the terms of the MIT License. See [LICENSE](LICENSE) for details.
