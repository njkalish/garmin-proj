from configparser import ConfigParser
from getpass import getpass
from pathlib import Path

from garminproj import config

credential_file_path = Path(config['User']['credential_file']).expanduser()


def create_credential_file(email, password):
    """
    Creates a credential file storing the Garmin Connect account email and
    password for logging in.
    """
    credentials = ConfigParser()
    credentials['Login'] = dict(
            email=email,
            password=password,
    )

    with credential_file_path.open('w') as file:
        credentials.write(file)

    return credential_file_path


def default_credentials():
    """
    Reads the default credentials from the saved credential file.
    """
    if not credential_file_path.exists():
        raise FileNotFoundError(
                f'Could not find configuration file at {credential_file_path}.'
                f'\nEnter email and password in create_credential_file to '
                f'create the file.'
        )

    garmin_connect_credentials = ConfigParser()
    garmin_connect_credentials.read(credential_file_path)

    return (garmin_connect_credentials['Login'][key]
            for key in ('email', 'password'))


def prompt_credentials():
    """
    Asks the user for credentials
    """
    email = getpass('Email: ')
    password = getpass('Password: ')
    return email, password
