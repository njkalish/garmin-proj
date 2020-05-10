from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from ._lap import Lap
from ._track_point import TrackPoint
from ._base import MyBase


class Activity(MyBase):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime, nullable=False)
    activity_type = Column(String)

    laps = relationship(
            "Lap", order_by=Lap.start_time, back_populates='activity'
    )

    track_points = relationship(
            "TrackPoint", order_by=TrackPoint.time, back_populates='activity'
    )

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
