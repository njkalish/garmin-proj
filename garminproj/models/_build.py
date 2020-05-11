from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ._base import Base
from .. import db_config

__all__ = ['session_scope', 'engine']

db_url = db_config['alembic']['sqlalchemy.url']
db_dir = db_config['alembic']['db_dir']

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
    db_path = Path(db_dir).expanduser()
    if not db_path.exists():
        db_path.mkdir(parents=True)

    Base.metadata.bind = engine
    Base.metadata.create_all()
