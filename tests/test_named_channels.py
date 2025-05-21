import unittest
from Stormworkspy import Stormworkspy


class TestNamedChannels(unittest.TestCase):
    def test_numeric_output_attribute(self):
        sw = Stormworkspy()
        sw.set_num_output("oMotor")
        sw.oMotor = 3.14
        self.assertEqual(sw.outnums[0], 3.14)
        self.assertEqual(sw.oMotor, 3.14)

    def test_bool_input_attribute(self):
        sw = Stormworkspy()
        sw.set_bool_input("iActive", index=1)
        sw.inbools[1] = True
        self.assertTrue(sw.iActive)

    def test_registration_limit(self):
        sw = Stormworkspy()
        for i in range(32):
            sw.set_num_output(f"ch{i}")
        with self.assertRaises(ValueError):
            sw.set_num_output("extra")


if __name__ == "__main__":
    unittest.main()
