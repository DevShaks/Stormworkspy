import unittest
import json
import time
import urllib.request
from Stormworkspy import Stormworkspy
from Stormworkspy.sensors import SW_LaserDistanceSensor

class TestChannelIndexing(unittest.TestCase):
    def test_channel_two_returns_one(self):
        sw = Stormworkspy()
        sw.register_sensor('distance', SW_LaserDistanceSensor, channel_distance=2)
        sw.run_api(host="127.0.0.1", port=5601)
        time.sleep(0.5)
        query = (
            "http://127.0.0.1:5601/?" +
            "num1=0.0&num2=1.0&num3=0.0&num4=0.0&num5=0.0&num6=0.0&num7=0.0&" +
            "num8=0.0&num9=0.0&num10=0.0&num11=0.0&num12=0.0&num13=0.0&num14=0.0&" +
            "num15=0.0&num16=0.0&num17=0.0&num18=0.0&num19=0.0&num20=0.0&num21=0.0&" +
            "num22=0.0&num23=0.0&num24=0.0&num25=0.0&num26=0.0&num27=0.0&num28=0.0&" +
            "num29=0.0&num30=0.0&num31=0.0&num32=0.0&" +
            "bool1=false&bool2=false&bool3=false&bool4=false&bool5=false&bool6=false&" +
            "bool7=false&bool8=false&bool9=false&bool10=false&bool11=false&bool12=false&" +
            "bool13=false&bool14=false&bool15=false&bool16=false&bool17=false&bool18=false&" +
            "bool19=false&bool20=false&bool21=false&bool22=false&bool23=false&bool24=false&" +
            "bool25=false&bool26=false&bool27=false&bool28=false&bool29=false&bool30=false&" +
            "bool31=false&bool32=false"
        )
        with urllib.request.urlopen(query) as resp:
            json.load(resp)
        self.assertEqual(sw.distance.get_distance(), 1.0)

if __name__ == "__main__":
    unittest.main()
