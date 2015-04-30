from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('pid', INTEGER, primary_key=True, nullable=False),
    Column('content', VARCHAR(length=140)),
    Column('posted', DATETIME),
    Column('belongs', INTEGER),
    Column('writer', INTEGER),
)

post = Table('post', post_meta,
    Column('pid', Integer, primary_key=True, nullable=False),
    Column('writer', Integer),
    Column('wid', Integer),
    Column('content', String(length=140)),
    Column('pic', String(length=1000)),
    Column('posted', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['belongs'].drop()
    post_meta.tables['post'].columns['pic'].create()
    post_meta.tables['post'].columns['wid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['belongs'].create()
    post_meta.tables['post'].columns['pic'].drop()
    post_meta.tables['post'].columns['wid'].drop()
