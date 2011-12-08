#coding=utf8

import time
import datetime
import StringIO

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc

from blog.models import DBSession
from blog.models import Post, Tag, Category

from docutils.core import publish_parts

import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

@view_config(route_name='test')
def test(request):
    import os
    html = open(os.path.join(os.path.dirname(__file__), 'templates/test.html')).read()
    return Response(html)

@view_config(route_name='index', renderer='blog:templates/base_new.mako')
def index(request):
    session = DBSession()
    posts = session.query(Post).order_by(desc(Post.timestamp))
    categories = session.query(Category)
    return dict(entries=posts, toplist=posts, categories=categories, tags=session.query(Tag))

@view_config(route_name='entry', renderer='blog:templates/entry.mako')
def entry(request):
    id = request.matchdict['kword_or_id']
    session = DBSession()
    entry = session.query(Post).get(id)
    posts = session.query(Post)
    entry.click_counter += 1
    session.flush()
    #f = StringIO.StringIO()
    #content = BlogHTMLParser().blogfeed(content, f, 2)
    return dict(entry=entry, toplist=posts,categories=session.query(Category), tags=session.query(Tag))

@view_config(route_name='post', renderer='blog:templates/post.mako')
def post(request):
    id = request.params.get('id')
    session = DBSession()
    if request.method == 'POST':
        title, content = request.POST['title'], request.POST['content']
        category, tags = request.POST['category'], request.POST['tags']
        p = None
        if id:
            p = session.query(Post).get(id)
        else:
            p = Post(timestamp=time.time(), date=datetime.date.today())
            session.add(p)
        p.title = title
        p.content = content
        if category and (not p.category or category != p.category.name):
            category = category.strip()
            c = session.query(Category).filter_by(name=category).first()
            if not c:
                c = Category(name=category)
            p.category = c
        if tags:
            tags = tags.split(',')
            tags = [v.strip() for v in tags]
            tags_db = []
            for tag in tags:
                t = session.query(Tag).filter_by(name=tag).first()
                if not t:
                    t = Tag(name=tag)
                tags_db.append(t)
            for i in range(len(p.tags)):
                p.tags.pop()
            for t in tags_db:
                p.tags.append(t)
        session.flush()
        return HTTPFound(location=request.route_url('index'))
    else:
        entry = None
        if id:
            entry = session.query(Post).get(id)
        return dict(entries=session.query(Post), entry=entry, toplist=session.query(Post))

from HTMLParser import HTMLParser
class BlogHTMLParser(HTMLParser):

    def blogfeed(self, data, fileobj, paragraph_num=1):
        self.paragraph_num = paragraph_num
        self.counter = 0
        self.f = fileobj
        return self.feed(data)

    def handle_starttag(self, tag, attrs):
        if self.counter == self.paragraph_num:
            return
        html = '<%s %s>'
        s_attrs = ''
        for k,v in attrs:
            s_attrs += ' %s="%s"'%(k,v)
        print >>self.f, html % (tag, s_attrs)

    def handle_data(self, data):
        if self.counter == self.paragraph_num:
            return
        print >>self.f, data

    def handle_endtag(self, tag):
        if self.counter == self.paragraph_num:
            return
        print >>self.f, '</%s>'%tag
        self.counter += 1
