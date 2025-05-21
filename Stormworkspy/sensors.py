def _idx(channel: int | None) -> int | None:
    """Convert a 1-based channel number to a zero-based index."""
    if channel is None:
        return None
    return channel - 1


class SW_PlayerSensor:
    """
    Player Sensor.
    Summary:
        Detects players within range. Supports setting detection mode (sphere/hemisphere, detect all/players/NPCs) and radius (0.25m to 10m).
    Wiki: https://stormworks.fandom.com/wiki/Player_Sensor

    Inputs (channel indices):
        None
    Outputs (values):
        players: Number of players detected
        detected: True if at least one player detected
    """
    def __init__(self, channel_players: int = None, channel_detected: int = None):
        self.channel_players = _idx(channel_players)
        self.channel_detected = _idx(channel_detected)
        # internal storage
        self._players = 0
        self._detected = False

    def get_players(self) -> int:
        return self._players

    def is_detected(self) -> bool:
        return self._detected

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_players is not None and self.channel_players < len(num_channels):
            self._players = int(num_channels[self.channel_players])
        if self.channel_detected is not None and self.channel_detected < len(bool_channels):
            self._detected = bool_channels[self.channel_detected]


class SW_WindSensor:
    """
    Wind Sensor.
    Summary:
        Measures relative wind direction and speed (m/s).
    Wiki: https://stormworks.fandom.com/wiki/Wind_Sensor

    Outputs (values):
        direction: Relative direction of the wind
        speed: Relative speed of the wind in m/s
    """
    def __init__(self, channel_direction: int = None, channel_speed: int = None):
        self.channel_direction = _idx(channel_direction)
        self.channel_speed = _idx(channel_speed)
        self._direction = 0.0
        self._speed = 0.0

    def get_direction(self) -> float:
        return self._direction

    def get_speed(self) -> float:
        return self._speed

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_direction is not None and self.channel_direction < len(num_channels):
            self._direction = num_channels[self.channel_direction]
        if self.channel_speed is not None and self.channel_speed < len(num_channels):
            self._speed = num_channels[self.channel_speed]


class SW_RainSensor:
    """
    Rain Sensor.
    Summary:
        Outputs rain intensity (0 = Sunny, 1 = Thunderstorm).
    Wiki: https://stormworks.fandom.com/wiki/Rain_Sensor

    Outputs (values):
        intensity: Rain intensity (0-1)
    """
    def __init__(self, channel_intensity: int = None):
        self.channel_intensity = _idx(channel_intensity)
        self._intensity = 0.0

    def get_intensity(self) -> float:
        return self._intensity

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_intensity is not None and self.channel_intensity < len(num_channels):
            self._intensity = num_channels[self.channel_intensity]


class SW_HumiditySensor:
    """
    Humidity Sensor.
    Summary:
        Measures fog density (0 = No fog, 1 = Max fog).
    Wiki: https://stormworks.fandom.com/wiki/Humidity_Sensor

    Outputs (values):
        humidity: Humidity value (0-1)
    """
    def __init__(self, channel_humidity: int = None):
        self.channel_humidity = _idx(channel_humidity)
        self._humidity = 0.0

    def get_humidity(self) -> float:
        return self._humidity

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_humidity is not None and self.channel_humidity < len(num_channels):
            self._humidity = num_channels[self.channel_humidity]


class SW_TemperatureSensor:
    """
    Temperature Sensor.
    Summary:
        Measures ambient temperature in °C.
    Wiki: https://stormworks.fandom.com/wiki/Temperature_Sensor

    Outputs (values):
        temperature: Ambient temperature in °C
    """
    def __init__(self, channel_temperature: int = None):
        self.channel_temperature = _idx(channel_temperature)
        self._temperature = 0.0

    def get_temperature(self) -> float:
        return self._temperature

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_temperature is not None and self.channel_temperature < len(num_channels):
            self._temperature = num_channels[self.channel_temperature]


class SW_TiltSensor:
    """
    Tilt Sensor.
    Summary:
        Outputs the tilt angle of the block (-0.25 for -90°, 0.25 for +90°).
    Wiki: https://stormworks.fandom.com/wiki/Tilt_Sensor

    Outputs (values):
        tilt: Tilt angle (-0.25 to 0.25)
    """
    def __init__(self, channel_tilt: int = None):
        self.channel_tilt = _idx(channel_tilt)
        self._tilt = 0.0

    def get_tilt(self) -> float:
        return self._tilt

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_tilt is not None and self.channel_tilt < len(num_channels):
            self._tilt = num_channels[self.channel_tilt]


class SW_PhysicsSensor:
    """
    Physics Sensor.
    Summary:
        Composite sensor for position, rotation, velocity, and angular velocity.
    Wiki: https://stormworks.fandom.com/wiki/Physics_Sensor

    Outputs (values):
        pos_x, pos_y, pos_z, rot_x, rot_y, rot_z,
        vel_x, vel_y, vel_z, angvel_x, angvel_y, angvel_z,
        speed_absolute, angspeed_absolute, pitch, roll, heading
    """
    def __init__(
        self,
        channel_pos_x: int = None,
        channel_pos_y: int = None,
        channel_pos_z: int = None,
        channel_rot_x: int = None,
        channel_rot_y: int = None,
        channel_rot_z: int = None,
        channel_vel_x: int = None,
        channel_vel_y: int = None,
        channel_vel_z: int = None,
        channel_angvel_x: int = None,
        channel_angvel_y: int = None,
        channel_angvel_z: int = None,
        channel_speed_absolute: int = None,
        channel_angspeed_absolute: int = None,
        channel_pitch: int = None,
        channel_roll: int = None,
        channel_heading: int = None,
    ):
        self.channel_pos_x = _idx(channel_pos_x)
        self.channel_pos_y = _idx(channel_pos_y)
        self.channel_pos_z = _idx(channel_pos_z)
        self.channel_rot_x = _idx(channel_rot_x)
        self.channel_rot_y = _idx(channel_rot_y)
        self.channel_rot_z = _idx(channel_rot_z)
        self.channel_vel_x = _idx(channel_vel_x)
        self.channel_vel_y = _idx(channel_vel_y)
        self.channel_vel_z = _idx(channel_vel_z)
        self.channel_angvel_x = _idx(channel_angvel_x)
        self.channel_angvel_y = _idx(channel_angvel_y)
        self.channel_angvel_z = _idx(channel_angvel_z)
        self.channel_speed_absolute = _idx(channel_speed_absolute)
        self.channel_angspeed_absolute = _idx(channel_angspeed_absolute)
        self.channel_pitch = _idx(channel_pitch)
        self.channel_roll = _idx(channel_roll)
        self.channel_heading = _idx(channel_heading)
        # internal storage
        self._values = {k: 0.0 for k in [
            'pos_x','pos_y','pos_z','rot_x','rot_y','rot_z',
            'vel_x','vel_y','vel_z','angvel_x','angvel_y','angvel_z',
            'speed_absolute','angspeed_absolute','pitch','roll','heading'
        ]}

    def get_all(self) -> dict:
        return dict(self._values)

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        for key, chan in [
            ('pos_x', self.channel_pos_x), ('pos_y', self.channel_pos_y), ('pos_z', self.channel_pos_z),
            ('rot_x', self.channel_rot_x), ('rot_y', self.channel_rot_y), ('rot_z', self.channel_rot_z),
            ('vel_x', self.channel_vel_x), ('vel_y', self.channel_vel_y), ('vel_z', self.channel_vel_z),
            ('angvel_x', self.channel_angvel_x), ('angvel_y', self.channel_angvel_y), ('angvel_z', self.channel_angvel_z),
            ('speed_absolute', self.channel_speed_absolute), ('angspeed_absolute', self.channel_angspeed_absolute),
            ('pitch', self.channel_pitch), ('roll', self.channel_roll), ('heading', self.channel_heading)
        ]:
            if chan is not None and chan < len(num_channels):
                self._values[key] = num_channels[chan]


class SW_LinearSpeedSensor:
    """
    Linear Speed Sensor.
    Summary:
        Measures speed with selectable modes (absolute, horizontal, vertical, directional).
    Wiki: https://stormworks.fandom.com/wiki/Linear_Speed_Sensor

    Outputs (values):
        speed: Speed in m/s
    """
    def __init__(self, channel_speed: int = None):
        self.channel_speed = _idx(channel_speed)
        self._speed = 0.0

    def get_speed(self) -> float:
        return self._speed

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_speed is not None and self.channel_speed < len(num_channels):
            self._speed = num_channels[self.channel_speed]


class SW_DistanceSensor:
    """
    Distance Sensor.
    Summary:
        Measures distance to the next block in the sensor's facing direction (up to 500m).
    Wiki: https://stormworks.fandom.com/wiki/Gameplay/Workbench/Components/Sensors#Distance_Sensor

    Outputs (values):
        distance: Distance in meters
    """
    def __init__(self, channel_distance: int = None):
        self.channel_distance = _idx(channel_distance)
        self._distance = 0.0

    def get_distance(self) -> float:
        return self._distance

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_distance is not None and self.channel_distance < len(num_channels):
            self._distance = num_channels[self.channel_distance]


class SW_LaserDistanceSensor:
    """
    Laser Distance Sensor.
    Summary:
        Similar to Distance Sensor but with range up to 4000m and laser beam effect.
    Wiki: https://stormworks.fandom.com/wiki/Laser_Distance_Sensor

    Outputs (values):
        distance: Distance in meters
    """
    def __init__(self, channel_distance: int = None):
        self.channel_distance = _idx(channel_distance)
        self._distance = 0.0

    def get_distance(self) -> float:
        return self._distance

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_distance is not None and self.channel_distance < len(num_channels):
            self._distance = num_channels[self.channel_distance]


class SW_LaserPointSensor:
    """
    Laser Point Sensor.
    Summary:
        Detects laser beacons and outputs their direction.
    Wiki: https://stormworks.fandom.com/wiki/Laser_Point_Sensor

    Outputs (values):
        direction: Direction to the beacon
    """
    def __init__(self, channel_direction: int = None):
        self.channel_direction = _idx(channel_direction)
        self._direction = 0.0

    def get_direction(self) -> float:
        return self._direction

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_direction is not None and self.channel_direction < len(num_channels):
            self._direction = num_channels[self.channel_direction]


class SW_CompassSensor:
    """
    Compass Sensor.
    Summary:
        Outputs orientation relative to north (-0.5 to 0.5). Optional backlight control input.
    Wiki: https://stormworks.fandom.com/wiki/Compass_Sensor

    Inputs (channel indices):
        channel_heading: Number
        channel_backlight: Boolean

    Outputs (values):
        heading: Orientation value
        backlight: Backlight on/off
    """
    def __init__(self, channel_heading: int = None, channel_backlight: int = None):
        self.channel_heading = _idx(channel_heading)
        self.channel_backlight = _idx(channel_backlight)
        self._heading = 0.0
        self._backlight = False

    def get_heading(self) -> float:
        return self._heading

    def is_backlight_on(self) -> bool:
        return self._backlight

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_heading is not None and self.channel_heading < len(num_channels):
            self._heading = num_channels[self.channel_heading]
        if self.channel_backlight is not None and self.channel_backlight < len(bool_channels):
            self._backlight = bool_channels[self.channel_backlight]


class SW_Altimeter:
    """
    Altimeter.
    Summary:
        Measures altitude relative to sea level.
    Wiki: https://stormworks.fandom.com/wiki/Altimeter

    Outputs (values):
        altitude: Altitude in meters
    """
    def __init__(self, channel_altitude: int = None):
        self.channel_altitude = _idx(channel_altitude)
        self._altitude = 0.0

    def get_altitude(self) -> float:
        return self._altitude

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_altitude is not None and self.channel_altitude < len(num_channels):
            self._altitude = num_channels[self.channel_altitude]


class SW_GPS:
    """
    GPS Sensor.
    Summary:
        Outputs X and Y world coordinates.
    Wiki: https://stormworks.fandom.com/wiki/GPS

    Outputs (values):
        x: X coordinate
        y: Y coordinate
    """
    def __init__(self, channel_x: int = None, channel_y: int = None):
        self.channel_x = _idx(channel_x)
        self.channel_y = _idx(channel_y)
        self._x = 0.0
        self._y = 0.0

    def get_position(self) -> tuple[float, float]:
        return (self._x, self._y)

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_x is not None and self.channel_x < len(num_channels):
            self._x = num_channels[self.channel_x]
        if self.channel_y is not None and self.channel_y < len(num_channels):
            self._y = num_channels[self.channel_y]


class SW_TorqueMeter:
    """
    Torque Meter.
    Summary:
        Measures rotations per second and torque force.
    Wiki: https://stormworks.fandom.com/wiki/Torque_Meter

    Outputs (values):
        rps: Rotations per second
        force: Torque force
    """
    def __init__(self, channel_rps: int = None, channel_force: int = None):
        self.channel_rps = _idx(channel_rps)
        self.channel_force = _idx(channel_force)
        self._rps = 0.0
        self._force = 0.0

    def get_rps(self) -> float:
        return self._rps

    def get_force(self) -> float:
        return self._force

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_rps is not None and self.channel_rps < len(num_channels):
            self._rps = num_channels[self.channel_rps]
        if self.channel_force is not None and self.channel_force < len(num_channels):
            self._force = num_channels[self.channel_force]


class SW_BasicRadar:
    """
    Basic Radar.
    Summary:
        Detects vehicles/persons; outputs bearing and distance.
    Wiki: https://stormworks.fANDOM.com/wiki/Basic_Radar

    Outputs (values):
        direction: Bearing to target
        distance: Distance to target
    """
    def __init__(self, channel_direction: int = None, channel_distance: int = None):
        self.channel_direction = _idx(channel_direction)
        self.channel_distance = _idx(channel_distance)
        self._direction = 0.0
        self._distance = 0.0

    def get_direction(self) -> float:
        return self._direction

    def get_distance(self) -> float:
        return self._distance

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_direction is not None and self.channel_direction < len(num_channels):
            self._direction = num_channels[self.channel_direction]
        if self.channel_distance is not None and self.channel_distance < len(num_channels):
            self._distance = num_channels[self.channel_distance]


class SW_PhalanxRadar:
    """
    Phalanx Radar.
    Summary:
        Medium-range radar for vehicles/persons detection.
    Wiki: https://stormworks.fANDOM.com/wiki/Phalanx_Radar

    Outputs (values):
        direction: Bearing
        distance: Distance
    """
    def __init__(self, channel_direction: int = None, channel_distance: int = None):
        self.channel_direction = _idx(channel_direction)
        self.channel_distance = _idx(channel_distance)
        self._direction = 0.0
        self._distance = 0.0

    def get_direction(self) -> float:
        return self._direction

    def get_distance(self) -> float:
        return self._distance

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_direction is not None and self.channel_direction < len(num_channels):
            self._direction = num_channels[self.channel_direction]
        if self.channel_distance is not None and self.channel_distance < len(num_channels):
            self._distance = num_channels[self.channel_distance]


class SW_RadarDish:
    """
    Radar Dish (Large Radar).
    Summary:
        Large radar unit for extended range detection.
    Wiki: https://stormworks.fANDOM.com/wiki/Radar_Dish

    Outputs (values):
        direction: Bearing
        distance: Distance
    """
    def __init__(self, channel_direction: int = None, channel_distance: int = None):
        self.channel_direction = _idx(channel_direction)
        self.channel_distance = _idx(channel_distance)
        self._direction = 0.0
        self._distance = 0.0

    def get_direction(self) -> float: return self._direction
    def get_distance(self) -> float: return self._distance

    def update(self, num_channels: list[float], bool_channels: list[bool]):
        if self.channel_direction is not None and self.channel_direction < len(num_channels): self._direction = num_channels[self.channel_direction]
        if self.channel_distance is not None and self.channel_distance < len(num_channels): self._distance = num_channels[self.channel_distance]


class SW_RadarAWACS:
    """
    Radar AWACS (Huge Radar).
    Summary:
        Huge radar for maximum detection range.
    Wiki: https://stormworks.fANDOM.com/wiki/Radar_AWACS

    Outputs (values):
        direction: Bearing
        distance: Distance
    """
    def __init__(self, channel_direction=None, channel_distance=None):
        self.channel_direction = _idx(channel_direction)
        self.channel_distance = _idx(channel_distance)
        self._direction = 0.0; self._distance = 0.0
    def get_direction(self): return self._direction
    def get_distance(self): return self._distance
    def update(self, num_channels, bool_channels):
        if self.channel_direction is not None and self.channel_direction < len(num_channels): self._direction = num_channels[self.channel_direction]
        if self.channel_distance is not None and self.channel_distance < len(num_channels): self._distance = num_channels[self.channel_distance]


class SW_MissileRadar:
    """
    Missile Radar.
    Summary:
        Compact radar for missile targeting.
    Wiki: https://stormworks.fANDOM.com/wiki/Missile_Radar

    Outputs (values):
        direction: Bearing
        distance: Distance
    """
    def __init__(self, channel_direction=None, channel_distance=None):
        self.channel_direction = _idx(channel_direction)
        self.channel_distance = _idx(channel_distance)
        self._direction = 0.0
        self._distance = 0.0
    def get_direction(self): return self._direction
    def get_distance(self): return self._distance
    def update(self, num_channels, bool_channels):
        if self.channel_direction!=None and self.channel_direction<len(num_channels): self._direction=num_channels[self.channel_direction]
        if self.channel_distance!=None and self.channel_distance<len(num_channels): self._distance=num_channels[self.channel_distance]


class SW_Sonar:
    """
    Sonar Sensor.
    Summary:
        Detects underwater objects; passive mode suppressed while pinging.
    Wiki: https://stormworks.fANDOM.com/wiki/Sonar

    Inputs (channel indices):
        channel_ping: Boolean to trigger ping
    Outputs (values):
        angle: Relative angle to object
    """
    def __init__(self, channel_ping=None, channel_angle=None):
        self.channel_ping = _idx(channel_ping)
        self.channel_angle = _idx(channel_angle)
        self._angle = 0.0
        self._ping = False
    def is_ping(self): return self._ping
    def get_angle(self): return self._angle
    def update(self, num_channels, bool_channels):
        if self.channel_ping!=None and self.channel_ping<len(bool_channels): self._ping=bool_channels[self.channel_ping]
        if self.channel_angle!=None and self.channel_angle<len(num_channels): self._angle=num_channels[self.channel_angle]


class SW_FluidPressureSensor:
    """
    Fluid Pressure Sensor.
    Summary:
        Measures fluid pressure in the surrounding room.
    Wiki: https://stormworks.fANDOM.com/wiki/Fluid_Pressure_Sensor

    Outputs (values):
        pressure: Pressure reading
    """
    def __init__(self, channel_pressure=None):
        self.channel_pressure = _idx(channel_pressure)
        self._pressure = 0.0
    def get_pressure(self): return self._pressure
    def update(self, num_channels, bool_channels):
        if self.channel_pressure!=None and self.channel_pressure<len(num_channels): self._pressure=num_channels[self.channel_pressure]


class SW_FluidMeter:
    """
    Fluid Meter.
    Summary:
        Outputs room capacity and current fluid amount.
    Wiki: https://stormworks.fANDOM.com/wiki/Fluid_Meter

    Outputs (values):
        capacity: Room capacity (L)
        amount: Fluid amount (L)
    """
    def __init__(self, channel_capacity=None, channel_amount=None):
        self.channel_capacity = _idx(channel_capacity)
        self.channel_amount = _idx(channel_amount)
        self._capacity = 0.0
        self._amount = 0.0
    def get_capacity(self): return self._capacity
    def get_amount(self): return self._amount
    def update(self, num_channels, bool_channels):
        if self.channel_capacity!=None and self.channel_capacity<len(num_channels): self._capacity=num_channels[self.channel_capacity]
        if self.channel_amount!=None and self.channel_amount<len(num_channels): self._amount=num_channels[self.channel_amount]


class SW_ClockSensor:
    """
    Clock Sensor.
    Summary:
        Outputs current time fraction (0 = 12am, 0.5 = 12pm).
    Wiki: https://stormworks.fANDOM.com/wiki/Clock

    Outputs (values):
        time: Fraction of day
    """
    def __init__(self, channel_time=None):
        self.channel_time = _idx(channel_time)
        self._time = 0.0
    def get_time(self): return self._time
    def update(self, num_channels, bool_channels):
        if self.channel_time!=None and self.channel_time<len(num_channels): self._time=num_channels[self.channel_time]

