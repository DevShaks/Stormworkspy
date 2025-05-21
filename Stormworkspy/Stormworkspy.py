import threading
from flask import Flask, Request, jsonify, request
import logging


class Stormworkspy():
    def __init__(self, name="default"):
        # mappings for named channels
        object.__setattr__(self, "num_out_names", {})
        object.__setattr__(self, "num_in_names", {})
        object.__setattr__(self, "bool_out_names", {})
        object.__setattr__(self, "bool_in_names", {})
        # registered sensors
        object.__setattr__(self, "sensors", {})

        self.name = name
        self.innums = [0.0] * 32
        self.inbools = [False] * 32
        self.outnums = [0.0] * 32
        self.outbools = [False] * 32

        self.app = Flask(__name__)
        self._setup_routes()
        self.thread = None
        self.host = None
        self.port = None

        # Disable the Werkzeug logger (Flask's default HTTP request log)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        log.disabled = True
        # Disable the Flask app logger
        self.app.logger.disabled = True

    # ------------------------------------------------------------------
    # Registration helpers
    def _register_name(self, mapping, name, index, length):
        if name in mapping:
            raise ValueError(f"{name} already registered")

        used = set(mapping.values())
        if index is None:
            for i in range(length):
                if i not in used:
                    index = i
                    break
            else:
                raise ValueError("No free slots available")
        else:
            if not 0 <= index < length:
                raise IndexError("index out of range")
            if index in used:
                raise ValueError(f"Index {index} already used")

        mapping[name] = index
        return index

    def set_num_output(self, name, index=None):
        """Register a numeric output channel name."""
        return self._register_name(self.num_out_names, name, index, 32)

    def set_bool_output(self, name, index=None):
        """Register a boolean output channel name."""
        return self._register_name(self.bool_out_names, name, index, 32)

    def set_num_input(self, name, index=None):
        """Register a numeric input channel name."""
        return self._register_name(self.num_in_names, name, index, 32)

    def set_bool_input(self, name, index=None):
        """Register a boolean input channel name."""
        return self._register_name(self.bool_in_names, name, index, 32)

    def register_sensor(self, name, sensor_cls, **channels):
        """Register a sensor and expose it as an attribute.

        The attribute type is added to class annotations so IDEs can offer
        autocompletion for the sensor's methods.
        """
        if name in self.sensors:
            raise ValueError(f"{name} already registered")
        sensor = sensor_cls(**channels)
        self.sensors[name] = sensor
        # update type hints for IDE autocompletion
        annotations = dict(getattr(self.__class__, "__annotations__", {}))
        annotations[name] = sensor_cls
        self.__class__.__annotations__ = annotations
        return sensor

    def _setup_routes(self):
        # Define the Flask route as a closure so it has access to self.
        @self.app.route('/', methods=['GET'])
        def sw_controller():
            # Update self.innums from GET parameters.
            for i in range(1, 33):
                param = f'num{i}'
                try:
                    self.innums[i - 1] = float(request.args.get(param, 0.0))
                except ValueError:
                    self.innums[i - 1] = 0.0
            
            # Update self.inbools from GET parameters.
            for i in range(1, 33):
                param = f'bool{i}'
                bool_str = request.args.get(param, "false").lower()
                self.inbools[i - 1] = bool_str in ["true", "1", "yes"]
            
            # Build the JSON response using self.outnums and self.outbools.
            response_data = {}
            for i in range(1, 33):
                response_data[f'num{i}'] = self.outnums[i - 1]
                response_data[f'bool{i}'] = str(self.outbools[i - 1]).lower()
            
            return jsonify(response_data)

        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            func = request.environ.get('werkzeug.server.shutdown')
            if func:
                func()
            return 'Server shutting down...'
        

    def run_api(self, host='localhost', port=5000, debug=False):
        def run():
            self.app.run(host=host, port=port, debug=debug)

        # Start the Flask app in a daemon thread so it runs in the background.
        self.host = host
        self.port = port
        self.thread = threading.Thread(target=run)
        self.thread.daemon = True
        self.thread.start()
        print(f"Flask API started on {host}:{port} in the background.")

    def stop_api(self):
        if not self.thread:
            return

        # Trigger Flask shutdown via the dedicated route
        try:
            import urllib.request
            req = urllib.request.Request(
                f'http://{self.host}:{self.port}/shutdown',
                method='POST'
            )
            urllib.request.urlopen(req)
        except Exception:
            pass

        self.thread.join()

    # ------------------------------------------------------------------
    # Attribute access for named channels
    def __getattr__(self, name):
        if name in self.sensors:
            sensor = self.sensors[name]
            sensor.update(self.innums, self.inbools)
            return sensor
        if name in self.num_out_names:
            return self.outnums[self.num_out_names[name]]
        if name in self.bool_out_names:
            return self.outbools[self.bool_out_names[name]]
        if name in self.num_in_names:
            return self.innums[self.num_in_names[name]]
        if name in self.bool_in_names:
            return self.inbools[self.bool_in_names[name]]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        mappings_ready = 'num_out_names' in self.__dict__
        if mappings_ready:
            if name in self.sensors:
                self.sensors[name] = value
                object.__setattr__(self, name, value)
                return
            if name in self.num_out_names:
                self.outnums[self.num_out_names[name]] = value
                return
            if name in self.bool_out_names:
                self.outbools[self.bool_out_names[name]] = value
                return
            if name in self.num_in_names:
                self.innums[self.num_in_names[name]] = value
                return
            if name in self.bool_in_names:
                self.inbools[self.bool_in_names[name]] = value
                return

        object.__setattr__(self, name, value)
