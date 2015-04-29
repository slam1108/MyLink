from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('pid', INTEGER, primary_key=True, nullable=False),
    Column('content', VARCHAR(length=140)),
    Column('posted', DATETIME),
    Column('uid', INTEGER),
)

post = Table('post', post_meta,
    Column('pid', Integer, primary_key=True, nullable=False),
    Column('writer', Integer),
    Column('belongs', Integer),
    Column('content', String(length=140)),
    Column('posted', DateTime),
)

user = Table('user', post_meta,
    Column('uid', Integer, primary_key=True, nullable=False),
    Column('firstname', String(length=100)),
    Column('lastname', String(length=100)),
    Column('email', String(length=120)),
    Column('password', String(length=54)),
    Column('pic', String(length=100)),
    Column('activate', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['uid'].drop()
    post_meta.tables['post'].columns['belongs'].create()
    post_meta.tables['post'].columns['writer'].create()
    post_meta.tables['user'].columns['activate'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['uid'].create()
    post_meta.tables['post'].columns['belongs'].drop()
    post_meta.tables['post'].columns['writer'].drop()
    post_meta.tables['user'].columns['activate'].drop()
