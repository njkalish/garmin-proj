from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ._lap import Lap
from ._track_point import TrackPoint
from ._base import MyBase


class Activity(MyBase):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime, nullable=False)
    sport = Column(String)

    laps = relationship(
            "Lap", order_by=Lap.start_time, back_populates='activity'
    )

    track_points = relationship(
            "TrackPoint", order_by=TrackPoint.time, back_populates='activity'
    )
