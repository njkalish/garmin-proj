from dateutil.parser import parse
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from ._base import Base
from ._build import session
from ._lap import Lap
from ._track_point import TrackPoint


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime, nullable=False)
    activity_type = Column(String)
    event_type = Column(String)
    distance = Column(Float)
    description = Column(String)
    duration = Column(Float)
    moving_duration = Column(Float)
    elevation_gain = Column(Float)
    elevation_loss = Column(Float)
    average_speed = Column(Float)
    max_speed = Column(Float)
    calories = Column(Integer)
    average_hr = Column(Integer)
    max_hr = Column(Integer)
    average_running_cadence = Column(Float)
    max_running_cadence = Column(Integer)
    steps = Column(Integer)
    aerobic_training_effect = Column(Float)
    anaerobic_training_effect = Column(Float)
    average_stride_length = Column(Float)
    vo2_max = Column(Integer)
    max_vertical_speed = Column(Float)
    water_estimated = Column(Integer)

    laps = relationship(
            "Lap", order_by=Lap.start_time, back_populates='activity'
    )

    track_points = relationship(
            "TrackPoint", order_by=TrackPoint.time, back_populates='activity'
    )

    @classmethod
    def from_garmin_json_dict(cls, json_dict, parse_tcx=True):
        from ..connect import get_activity_tcx_data

        if isinstance(json_dict, list):
            return [cls.from_garmin_json_dict(json, parse_tcx=parse_tcx)
                    for json in json_dict]

        obj = cls()

        obj.id = json_dict['activityId']
        obj.name = json_dict['activityName']
        obj.datetime = parse(json_dict['startTimeLocal'])
        obj.activity_type = json_dict['activityType']['typeKey']
        obj.event_type = json_dict['eventType']['typeKey']
        obj.distance = json_dict['distance']
        obj.description = json_dict['description']
        obj.duration = json_dict['duration']
        obj.moving_duration = json_dict['movingDuration']
        obj.elevation_gain = json_dict['elevationGain']
        obj.elevation_loss = json_dict['elevationLoss']
        obj.average_speed = json_dict['averageSpeed']
        obj.max_speed = json_dict['maxSpeed']
        obj.calories = json_dict['calories']
        obj.average_hr = json_dict['averageHR']
        obj.max_hr = json_dict['maxHR']
        obj.average_running_cadence = json_dict['averageRunningCadenceInStepsPerMinute']
        obj.max_running_cadence = json_dict['maxRunningCadenceInStepsPerMinute']
        obj.steps = json_dict['steps']
        obj.aerobic_training_effect = json_dict['aerobicTrainingEffect']
        obj.anaerobic_training_effect = json_dict['anaerobicTrainingEffect']
        obj.average_stride_length = json_dict['avgStrideLength']
        obj.vo2_max = json_dict['vO2MaxValue']
        obj.max_vertical_speed = json_dict['maxVerticalSpeed']
        obj.water_estimated = json_dict['waterEstimated']

        session.add(obj)
        if not parse_tcx:
            return obj

        tcx = get_activity_tcx_data(obj.id)

        for tcx_lap in tcx.activities[0].laps:
            lap = Lap(
                    activity_id=obj.id,
                    lap_number=tcx_lap.lap_number,
                    start_time=tcx_lap.start_time,
                    lap_seconds=tcx_lap.lap_seconds,
                    lap_meters=tcx_lap.lap_meters,
                    max_speed=tcx_lap.max_speed,
                    calories=tcx_lap.calories,
                    avg_hr=tcx_lap.avg_hr,
                    max_hr=tcx_lap.max_hr,
                    intensity=tcx_lap.intensity,
                    trigger_method=tcx_lap.trigger_method,
            )
            session.add(lap)

            for track_point in tcx_lap.track_points:
                tp = TrackPoint(
                        activity_id=obj.id,
                        lap_id=lap.id,
                        time=track_point.time,
                        hr=track_point.hr,
                        cadence=track_point.cadence,
                        speed=track_point.speed,
                        distance=track_point.distance,
                        altitude=track_point.altitude,
                        latitude=track_point.latitude,
                        longitude=track_point.longitude,
                )
                session.add(tp)

        return obj
