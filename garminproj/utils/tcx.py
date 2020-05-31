from os import PathLike

from dateutil.parser import parse
from lxml import objectify


def none_if_error(error_types=(AttributeError, ValueError, TypeError)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_types:
                return None

        return wrapper

    return decorator


class TCXFile:
    def __init__(self, file: PathLike):
        self.tree = objectify.parse(file)
        self.root = self.tree.getroot()

        self.activities = [_TCXActivity(item)
                           for item in self.root.Activities.Activity]


class _TCXActivity:
    def __init__(self, element):
        self.element = element
        self.laps = [_TCXLap(item, self) for item in self.element.Lap]

    @property
    def datetime(self):
        return parse(str(self.element.Id))

    @property
    def sport(self):
        return self.element.attrib['Sport']


class _TCXLap:
    def __init__(self, element, activity):
        self.element = element
        self.activity = activity

        self.track_points = [_TCXTrackPoint(item, self)
                             for item in self.element.Track.Trackpoint]

    @property
    @none_if_error()
    def lap_number(self):
        return self.activity.element.index(self.element)

    @property
    @none_if_error()
    def start_time(self):
        return parse(self.element.attrib['StartTime']) - self.activity.datetime

    @property
    @none_if_error()
    def lap_seconds(self):
        return float(self.element.TotalTimeSeconds)

    @property
    @none_if_error()
    def lap_meters(self):
        return float(self.element.DistanceMeters)

    @property
    @none_if_error()
    def max_speed(self):
        try:
            return float(self.element.MaximumSpeed)
        except (AttributeError):
            return None

    @property
    @none_if_error()
    def calories(self):
        return int(self.element.Calories)

    @property
    @none_if_error()
    def avg_hr(self):
        return int(self.element.AverageHeartRateBpm.Value)

    @property
    @none_if_error()
    def max_hr(self):
        return int(self.element.MaximumHeartRateBpm.Value)

    @property
    @none_if_error()
    def intensity(self):
        return str(self.element.Intensity)

    @property
    @none_if_error()
    def trigger_method(self):
        return str(self.element.TriggerMethod)


class _TCXTrackPoint:
    def __init__(self, element, lap):
        self.element = element
        self.lap = lap
        self.activity = lap.activity

    @property
    @none_if_error()
    def time(self):
        return parse(str(self.element.Time)) - self.activity.datetime

    @property
    @none_if_error()
    def hr(self):
        return int(self.element.HeartRateBpm.Value)

    @property
    def _tpx(self):
        return self.element.Extensions.getchildren()[0]

    @property
    @none_if_error()
    def cadence(self):
        return 2 * int(self._tpx.find('ns3:RunCadence', namespaces=self._tpx.nsmap))

    @property
    @none_if_error()
    def speed(self):
        return float(self._tpx.find('ns3:Speed', namespaces=self._tpx.nsmap))

    @property
    @none_if_error()
    def distance(self):
        return self.element.DistanceMeters

    @property
    @none_if_error()
    def altitude(self):
        return float(self.element.AltitudeMeters)

    @property
    @none_if_error()
    def latitude(self):
        return float(self.element.Position.LatitudeDegrees)

    @property
    @none_if_error()
    def longitude(self):
        return float(self.element.Position.LongitudeDegrees)
