import unittest
from Stormworkspy import Stormworkspy
from Stormworkspy.sensors import SW_LaserDistanceSensor, SW_Altimeter


class TestSensorRegistration(unittest.TestCase):
    def test_register_and_access_sensor(self):
        sw = Stormworkspy()
        sensor = sw.register_sensor('distance', SW_LaserDistanceSensor, channel_distance=0)
        sw.innums[0] = 42.0
        self.assertIs(sw.distance, sensor)
        self.assertEqual(sw.distance.get_distance(), 42.0)
        self.assertIs(sw.__class__.__annotations__['distance'], SW_LaserDistanceSensor)

    def test_duplicate_registration(self):
        sw = Stormworkspy()
        sw.register_sensor('alt', SW_Altimeter, channel_altitude=0)
        with self.assertRaises(ValueError):
            sw.register_sensor('alt', SW_Altimeter, channel_altitude=1)


if __name__ == '__main__':
    unittest.main()
