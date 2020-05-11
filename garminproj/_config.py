from configparser import ConfigParser
from pathlib import Path

project_path = Path(__file__).parents[1]

config = ConfigParser()
config.read(project_path / 'config.ini')

db_config = ConfigParser()

db_config.read(project_path / 'alembic.ini')