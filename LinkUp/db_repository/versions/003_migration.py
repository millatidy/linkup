from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('social_id', VARCHAR(length=64)),
    Column('username', VARCHAR(length=64)),
    Column('nickname', VARCHAR(length=64), nullable=False),
    Column('email', VARCHAR(length=64)),
    Column('about', VARCHAR(length=120)),
    Column('website', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=64)),
    Column('username', String(length=64)),
    Column('nickname', String(length=64), nullable=False),
    Column('email', String(length=64)),
    Column('website', String(length=64)),
    Column('bio', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['about'].drop()
    post_meta.tables['user'].columns['bio'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['about'].create()
    post_meta.tables['user'].columns['bio'].drop()
