#coding=utf8


import os
import sys
import time
import datetime
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Tag,
    Post,
    Base,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        tag = Tag(name='start from here')
        DBSession.add(tag)
        post = Post(title='Hello world!', content='''
**welcome**

- writen posts by reStructText 
- python and pyramid are used for building this blog''',
                timestamp=time.time(), date=datetime.datetime.today(),
                url_kword="start-from-here",
                summary="Hellow world post.",
                )
        post.tags.append(tag)
        DBSession.add(post)
        post = Post(title='', content='''
======
Title
======


.. contents::


A new start from here
=====================

- It's cool
- It's simple
- It's fast

Right, reStructText
===================

Guess right?
'''
            , timestamp=time.time(),
            date=datetime.datetime.today(), url_kword="new-start-post",
            summary="Another hello world test post."
            )
        post.tags.append(tag)
        DBSession.add(post)
