from warnings import warn

from click import confirm, echo
from garminconnect import Garmin, GarminConnectConnectionError, \
    GarminConnectTooManyRequestsError, GarminConnectAuthenticationError
from requests import HTTPError

from garminproj.connect.auth import default_credentials, prompt_credentials, \
    credential_file_path, create_credential_file


def get_connect_session():
    """
    General access point for getting an authenticated Garmin Connect session.

    Returns
    -------
    session : Garmin
        Connected Garmin Connect API object
    """

    # 1. If an email / password is stored, attempt to login with the credentials
    while True:
        try:
            session = Garmin(*default_credentials())
            session.login()
            return session

        except FileNotFoundError:
            # No credential file created
            break

        except (GarminConnectAuthenticationError,
                HTTPError):
            # Invalid authentication
            warn(
                    f'Default credentials in {credential_file_path} are invalid.'
                    f' Please update.',
                    UserWarning
            )
            break

    # 2. Try entering credentials manually.
    while True:
        email, password = prompt_credentials()
        try:
            session = Garmin(email, password)
            session.login()

            save = confirm('Do you want to save these credentials?')

            if save:
                save_file_path = create_credential_file(email, password)
                echo(f'Email and password saved to {save_file_path}')

            return session

        except (
                GarminConnectConnectionError,
                GarminConnectAuthenticationError,
                GarminConnectTooManyRequestsError,
                HTTPError
        ) as err:
            print("Error occured during Garmin Connect Client login: %s" % err)
