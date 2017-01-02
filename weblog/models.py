#coding=utf8

import datetime

from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Index,
    Unicode,
    Integer,
    UnicodeText,
    Table,
    ForeignKey,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
Base = declarative_base()


class Tag(Base):
    __tablename__ = 't_tag'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(55))
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)


rel_post_tag = Table('r_post_tag', Base.metadata,
        Column('post_id', Integer, ForeignKey('t_post.id')),
        Column('tag_id', Integer, ForeignKey('t_tag.id'))
        )


class Post(Base):
    __tablename__ = 't_post'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    url_kword = Column(Unicode(55), unique=True, nullable=False)
    summary = Column(Unicode(140))
    content = Column(UnicodeText)
    tags = relationship('Tag', secondary=lambda: rel_post_tag, backref='posts')
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)

