from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import db_config

__all__ = ['session']

engine = create_engine(db_config['alembic']['sqlalchemy.url'], echo=True)

Session = sessionmaker(engine)
session = Session()
