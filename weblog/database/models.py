import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import (
    Column,
    Index,
    Unicode,
    Integer,
    UnicodeText,
    Table,
    ForeignKey,
    DateTime,
    LargeBinary,
)

from .meta import Base


class Tag(Base):
    __tablename__ = "t_tag"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(55))
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    timestamp = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )


rel_post_tag = Table(
    "r_post_tag",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("t_post.id")),
    Column("tag_id", Integer, ForeignKey("t_tag.id")),
    UniqueConstraint("post_id", "tag_id", name="uk_r_post_tag"),
)


class Post(Base):
    __tablename__ = "t_post"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    url_kword = Column(Unicode(55), unique=True, nullable=False)
    summary = Column(Unicode(140))
    content = Column(UnicodeText)
    tags = relationship("Tag", secondary=lambda: rel_post_tag, backref="posts")
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    timestamp = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )


class Image(Base):
    __tablename__ = "t_image"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100))
    md5 = Column(Unicode(32), unique=True)
    image_raw = Column(LargeBinary)
    image_thumbnail = Column(LargeBinary)
    image_ext = Column(Unicode(5))
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    timestamp = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )


Index("image_md5", Image.md5, unique=True)
