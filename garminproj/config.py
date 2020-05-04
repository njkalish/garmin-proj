from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

db_config = ConfigParser()
db_config.read('alembic.ini')