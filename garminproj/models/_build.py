from contextlib import contextmanager
from pathlib import Path
from urllib import parse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ._base import Base
from .. import config

__all__ = ['session_scope', 'engine']


def _db_dir():
    project_path = Path(__file__).parents[2]
    return project_path / config['alembic']['db_dir']


def _db_url():
    """
    Returns the database url absolute path to the project folder
    """
    relative_url = parse.urlsplit(config['alembic']['sqlalchemy.url'])
    project_path = Path(__file__).parents[2]
    absolute_path = (project_path / relative_url.path[1:]).as_posix()

    return relative_url.scheme + ':///' + absolute_path


db_dir = _db_dir()
db_url = _db_url()

engine = create_engine(db_url, echo=True)
Session = sessionmaker(engine, expire_on_commit=False)


@contextmanager
def session_scope():
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
    # Storing database within project
    if not db_dir.exists():
        db_dir.mkdir(parents=True)

    Base.metadata.bind = engine
    Base.metadata.create_all()
