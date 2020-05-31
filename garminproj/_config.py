from configparser import ConfigParser
from pathlib import Path

project_path = Path(__file__).parents[1]

config = ConfigParser()
config.read([str(project_path / 'config.ini')])
config.read([str(project_path / 'alembic.ini')])
