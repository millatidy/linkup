from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('description', VARCHAR(length=120)),
    Column('venu', VARCHAR(length=64)),
    Column('date', DATETIME),
    Column('end_time', DATETIME),
    Column('admission', VARCHAR(length=20)),
    Column('category', VARCHAR(length=20)),
    Column('user_id', INTEGER),
)

event = Table('event', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('description', String(length=120)),
    Column('date', DateTime),
    Column('end_time', DateTime),
    Column('admission', String(length=20), default=ColumnDefault('free')),
    Column('category', String(length=20)),
    Column('user_id', Integer),
    Column('location_id', Integer),
)

location = Table('location', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=120)),
    Column('latitue', DECIMAL(precision=6, scale=4)),
    Column('longitude', DECIMAL(precision=7, scale=4)),
)

location = Table('location', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('latitude', DECIMAL(precision=6, scale=4)),
    Column('longitude', DECIMAL(precision=7, scale=4)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['venu'].drop()
    post_meta.tables['event'].columns['location_id'].create()
    pre_meta.tables['location'].columns['latitue'].drop()
    post_meta.tables['location'].columns['latitude'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['event'].columns['venu'].create()
    post_meta.tables['event'].columns['location_id'].drop()
    pre_meta.tables['location'].columns['latitue'].create()
    post_meta.tables['location'].columns['latitude'].drop()
