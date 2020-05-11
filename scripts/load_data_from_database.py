"""
Example of querying the database
"""

import garminproj as gp

min_hr = 150
min_calories = 500

with gp.session_scope() as session:
    for activity in session.query(gp.Activity) \
            .filter(gp.Activity.average_hr > min_hr) \
            .filter(gp.Activity.calories > min_calories).all():

        print(
                activity.name,
                f'date: {activity.datetime}'
                f'average_hr: {activity.average_hr}',
                f'calories burned: {activity.calories}'
        )

    hrs = [tp.hr for tp in activity.track_points]
