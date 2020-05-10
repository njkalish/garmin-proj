from io import BytesIO

from requests import HTTPError

from .login import garmin_session

def get_latest_activities(number_of_activities=10):
    # From the session, guery the last activities
    query_url = garmin_session.url_activities + f'?limit={number_of_activities}'
    response = garmin_session.req.get(query_url)
    _check_response(response)

    return response.json()


def get_activity_tcx_data(activity_id):
    url = f'https://connect.garmin.com/modern/proxy/download-service/export/' \
        f'tcx/activity/{activity_id}'

    response = garmin_session.req.get(url=url)
    _check_response(response)

    return BytesIO(response.content)


def _check_response(response):
    if response.status_code != 200:
        raise HTTPError(response.status_code, response.reason)
