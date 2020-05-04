"""create activity table

Revision ID: 0e75700ff095
Revises: 
Create Date: 2020-05-02 18:34:25.082195

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.exc import OperationalError

# revision identifiers, used by Alembic.
revision = '0e75700ff095'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            'activities',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String),
            sa.Column('datetime', sa.DateTime, nullable=False),
            sa.Column('sport', sa.String)
    )

    op.create_table(
            'laps',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('activity_id', sa.Integer, sa.ForeignKey('activity.id')),
            sa.Column('lap_number', sa.Integer),
            sa.Column('start_time', sa.DateTime),
            sa.Column('lap_seconds', sa.Float),
            sa.Column('lap_meters', sa.Float),
            sa.Column('max_speed', sa.Float),
            sa.Column('calories', sa.Integer),
            sa.Column('avg_hr', sa.Integer),
            sa.Column('max_hr', sa.Integer),
            sa.Column('intensity', sa.String),
            sa.Column('trigger_method', sa.String)
    )

    op.create_table(
            'track_points',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('activity_id', sa.Integer, sa.ForeignKey('activity.id')),
            sa.Column('lap_id', sa.Integer, sa.ForeignKey('lap.id')),
            sa.Column('time', sa.DateTime),
            sa.Column('hr', sa.Integer),
            sa.Column('cadence', sa.Integer),
            sa.Column('speed', sa.Float),
            sa.Column('distance', sa.Float),
            sa.Column('altitude', sa.Float),
            sa.Column('latitude', sa.Float),
            sa.Column('longitude', sa.Float)
    )


def downgrade():
    for table in ['track_points', 'laps', 'activities']:
        try:
            op.drop_table(table)
        except OperationalError:
            pass
