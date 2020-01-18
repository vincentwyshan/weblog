import datetime

from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    UnicodeText,
    DateTime,
)

from .meta import Base


class Draft(Base):
    __tablename__ = "t_draft"
    id = Column(Integer, primary_key=True)

    title = Column(Unicode(255), nullable=False)
    url_kword = Column(Unicode(55), unique=True, nullable=False)
    summary = Column(Unicode(140))
    content = Column(UnicodeText)
    tags = Column(Unicode(300))

    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    timestamp = Column(
        DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )

