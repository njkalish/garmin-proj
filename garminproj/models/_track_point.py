from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ._base import MyBase


class TrackPoint(MyBase):
    __tablename__ = 'track_points'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    lap_id = Column(Integer, ForeignKey('laps.id'))
    time = Column(DateTime)
    hr = Column(Integer)
    cadence = Column(Integer)
    speed = Column(Float)
    distance = Column(Float)
    altitude = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)

    activity = relationship(
            'Activity', back_populates='track_points'
    )

    lap = relationship(
            'Lap', back_populates='track_points'
    )
