from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('rid', INTEGER, primary_key=True, nullable=False),
    Column('sender', INTEGER),
    Column('receiver', INTEGER),
    Column('connected', BOOLEAN),
    Column('sent', BOOLEAN),
    Column('confirmed', BOOLEAN),
)

request = Table('request', post_meta,
    Column('rid', Integer, primary_key=True, nullable=False),
    Column('sender', Integer),
    Column('receiver', Integer),
    Column('done', Boolean),
    Column('connected', Boolean),
    Column('sent', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['request'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['request'].drop()
