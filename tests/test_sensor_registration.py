import unittest
from Stormworkspy import Stormworkspy
from Stormworkspy.sensors import SW_Altimeter

class TestSensorRegistration(unittest.TestCase):
    def test_register_and_access_sensor(self):
        sw = Stormworkspy()
        sw.register_sensor('alt', SW_Altimeter, channel_altitude=0)
        sw.innums[0] = 123.4
        sensor = sw.alt
        self.assertIsInstance(sensor, SW_Altimeter)
        self.assertEqual(sensor.get_altitude(), 123.4)

if __name__ == '__main__':
    unittest.main()
