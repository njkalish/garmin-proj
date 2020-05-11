"""
This script shows the downloading capability. Run this script before querying
the database if you want anything interesting to happen.

You will need a Garmin Connect account, and it should probably have some
activities logged. If no activities are logged, go outside and play, and come
back with some data.
"""

import garminproj as gp

# This is an initial setup that only needs to be run the first time to create
# the database. Running it again will not hurt. There are other ways to create
# the database for the first time (see alembic folder)
gp.build_db()


# Download a bunch of activities from Garmin. These will be added to the
# database. If this is the first time, you will be prompted to enter your
# credentials. These will be saved to a configured location (see config.ini).
activities = gp.Activity.from_garmin_client(
        number_of_activities=10,
        download_tcx=True
)

# `activities` is a list of Activity table objects -- as many activities as
# could be found.

# Check out the first one -- these are ordered from earliest to latest.
activity = activities[0]


# Access the track points associated with the activity
track_points = activity.track_points

# Look at the last track point
print(track_points[-1])
