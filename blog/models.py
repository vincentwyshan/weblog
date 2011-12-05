import datetime

import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Text
from sqlalchemy import DATE
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

rel_post_tag = Table('rel_post_tag', Base.metadata,
        Column('post_id', Integer, ForeignKey('post.id')),
        Column('tag_id', Integer, ForeignKey('tag.id'))
        )

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(55))

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(55))

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    subtitle = Column(Unicode(255))
    url_kword = Column(Unicode(55))
    content = Column(Text)
    timestamp = Column(Integer, nullable=False)
    date = Column(DATE, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category')
    tags = relationship('Tag', secondary=lambda:rel_post_tag, backref='posts')
    click_counter = Column(Integer, default=0)


def populate():
    session = DBSession()
    #model = MyModel(name=u'root', value=55)
    import time
    q = session.query(Post).filter_by(title='Hello world')
    if q.count() == 0:
        session.bind.execute('delete from post')
        tag = Tag(name='Test')
        session.add(tag)
        category = Category(name='Foo bar')
        session.add(category)
        post = Post(title='Hello world', content='welcome\n=======\n- hello world!\n- Burn it',
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
