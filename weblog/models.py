#coding=utf8

import time

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    DATE,
    Table,
    ForeignKey,
    )


from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(55))

rel_post_tag = Table('rel_post_tag', Base.metadata,
        Column('post_id', Integer, ForeignKey('post.id')),
        Column('tag_id', Integer, ForeignKey('tag.id'))
        )

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    url_kword = Column(Unicode(55))
    summary = Column(Text)
    content = Column(Text) #REST content
    timestamp = Column(Integer, nullable=False)
    date = Column(DATE, nullable=False)
    tags = relationship('Tag', secondary=lambda:rel_post_tag, backref='posts')
    click_counter = Column(Integer, default=0)


def populate():
    session = DBSession()
    q = session.query(Post)
    if q.count() == 0:
        session.bind.execute('delete from post')
        session.bind.execute('delete from category')
        session.bind.execute('delete from tag')
        session.bind.execute('delete from rel_post_tag')
        tag = Tag(name='start from here')
        session.add(tag)
        post = Post(title='Hello world!', content='''
**welcome**

- writen posts by reStructText 
- python and pyramid are used for building this blog''',
                timestamp=time.time(), date=datetime.datetime.today())
        post.tags.append(tag)
        post.category = category
        #session.add(model)
        session.add(post)
        session.flush()
    transaction.commit()

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        transaction.abort() 
