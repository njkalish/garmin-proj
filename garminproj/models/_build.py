from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ._base import Base
from .. import db_config

engine = create_engine(db_config['alembic']['sqlalchemy.url'], echo=True)

Session = sessionmaker(engine, expire_on_commit=False)
session = Session()


def build_db():
    Base.metadata.bind = engine
    Base.metadata.create_all()
