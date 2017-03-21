from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
location = Table('location', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=120)),
    Column('latitude', String(length=8)),
    Column('longitude', String(length=9)),
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['location'].create()
    post_meta.tables['event'].columns['location_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['location'].drop()
    post_meta.tables['event'].columns['location_id'].drop()
