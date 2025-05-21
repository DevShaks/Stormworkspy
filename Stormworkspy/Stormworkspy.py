import threading
from flask import Flask, Request, jsonify, request
import logging


class Stormworkspy():
    def __init__(self, name = "default"):
        self.nema = name
        self.innums = [0.0] * 32
        self.inbools = [False] * 32
        self.outnums = [0.0] * 32
        self.outbools = [False] * 32

        self.app = Flask(__name__)
        self._setup_routes()
        self.thread = None

        # Disable the Werkzeug logger (Flask's default HTTP request log)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        log.disabled = True
        # Disable the Flask app logger
        self.app.logger.disabled = True

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
        

    def run_api(self, host='localhost', port=5000, debug=False):
        def run():
            self.app.run(host=host, port=port, debug=debug)
        
        # Start the Flask app in a daemon thread so it runs in the background.
        self.thread = threading.Thread(target=run)
        self.thread.daemon = True
        self.thread.start()
        print(f"Flask API started on {host}:{port} in the background.")

    def stop_api(self):
        """Stop the background Flask server if it is running."""
        if self.thread and self.thread.is_alive():
            # The Flask development server does not provide a direct shutdown
            # mechanism. This method waits for the thread to finish if it has
            # been signaled to stop elsewhere.
            self.thread.join(timeout=0)
