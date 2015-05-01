from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post__circle = Table('post__circle', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('pid', INTEGER),
    Column('cid', INTEGER),
)

post__circle = Table('post__circle', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('uid', Integer),
    Column('cid', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post__circle'].columns['pid'].drop()
    post_meta.tables['post__circle'].columns['uid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post__circle'].columns['pid'].create()
    post_meta.tables['post__circle'].columns['uid'].drop()
