from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ._base import Base
from .. import db_config

__all__ = ['session_scope', 'engine']

engine = create_engine(db_config['alembic']['sqlalchemy.url'], echo=True)
Session = sessionmaker(engine, expire_on_commit=False)


@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def build_db():
    Base.metadata.bind = engine
    Base.metadata.create_all()
