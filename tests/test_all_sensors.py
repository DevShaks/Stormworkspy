import unittest
import inspect
from Stormworkspy import sensors as sensors_module


class TestAllSensors(unittest.TestCase):
    BOOL_PARAMS = {"channel_detected", "channel_backlight", "channel_ping"}

    def setUp(self):
        self.num_channels = [float(i + 10) for i in range(32)]
        self.bool_channels = [i % 2 == 0 for i in range(32)]

    def test_sensors_update(self):
        sensor_classes = [cls for name, cls in vars(sensors_module).items() if name.startswith("SW_")]
        for cls in sensor_classes:
            sig = inspect.signature(cls.__init__)
            kwargs = {}
            num_idx = 0
            bool_idx = 0
            mapping = {}
            for param_name in sig.parameters:
                if param_name == "self":
                    continue
                if param_name in self.BOOL_PARAMS:
                    kwargs[param_name] = bool_idx
                    mapping[param_name] = bool_idx
                    bool_idx += 1
                else:
                    kwargs[param_name] = num_idx
                    mapping[param_name] = num_idx
                    num_idx += 1
            sensor = cls(**kwargs)
            sensor.update(self.num_channels, self.bool_channels)
            for param, idx in mapping.items():
                key = param[len("channel_") :]
                if hasattr(sensor, "_values"):
                    expected = self.num_channels[idx]
                    self.assertEqual(sensor._values[key], expected, f"{cls.__name__}.{key}")
                else:
                    expected = self.bool_channels[idx] if param in self.BOOL_PARAMS else self.num_channels[idx]
                    attr_name = "_" + key
                    self.assertEqual(getattr(sensor, attr_name), expected, f"{cls.__name__}.{key}")


if __name__ == "__main__":
    unittest.main()
