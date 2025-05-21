import os
import time

from Stormworkspy.Stormworkspy import Stormworkspy
from Stormworkspy.sensors import SW_LaserDistanceSensor

sw = Stormworkspy()

# The laser-distance sensor is wired to numeric channel 2 (num2 in the HTTP query)
sw.register_sensor("distance", SW_LaserDistanceSensor, channel_distance=2)

# Listen on *all* interfaces so 127.0.0.1 and ::1 both work
sw.run_api(host="0.0.0.0", port=5000, debug=False)

try:
    while True:
        # fetch the latest value (accessing sw.distance auto-updates the sensor)
        dist = sw.distance.get_distance()

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Laser distance on channel 2 → {dist}")
        print(f"raw numeric buffer        → {sw.innums}")

        # give Flask a chance to run & keep output readable
        time.sleep(0.1)

except KeyboardInterrupt:
    sw.stop_api()
