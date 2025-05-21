import unittest
import json
import time
import urllib.request
from Stormworkspy import Stormworkspy


class TestHTTPAPI(unittest.TestCase):
    def test_api_updates_and_returns(self):
        sw = Stormworkspy()
        sw.outnums[0] = 1.23
        sw.outbools[0] = True
        sw.run_api(host="127.0.0.1", port=5599)
        time.sleep(0.5)
        with urllib.request.urlopen("http://127.0.0.1:5599/?num1=42&bool1=true") as resp:
            data = json.load(resp)
        self.assertEqual(data["num1"], 1.23)
        self.assertEqual(data["bool1"], "true")
        self.assertEqual(sw.innums[0], 42.0)
        self.assertTrue(sw.inbools[0])


if __name__ == "__main__":
    unittest.main()
