#coding=utf8

import re
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

def sidebar_variables(func):
    def _warper(*kargs, **kwarg):
        response_dict = func(kargs[1]) #TODO here might be a pyramid bug
        session = DBSession()
        categories = []
        for category in session.query(Category):
            category.postcount = session.bind.execute("select count(0) from post where category_id=%s" % category.id).fetchone()[0]
            categories.append(category)
        archives = {}
        for p in session.query(Post):
            a_d = datetime.datetime.fromtimestamp(p.timestamp).strftime("%B %Y")
            if a_d in archives:
                archives[a_d] += 1
            else:
                archives[a_d] = 1
        tmp_archives = []
        for a,cnt in archives.items():
            tmp_archives.append((a, cnt))
        response_dict.update({'categories':categories, 'archives':tmp_archives })
        if not 'recent_posts' in response_dict:
            response_dict['recent_posts'] = session.query(Post).order_by(desc(Post.timestamp))
        if not 'current_query' in response_dict:
            response_dict['current_query'] = {}
        return response_dict
    return _warper

@view_config(route_name='index', renderer='blog:templates/base_new.mako')
@sidebar_variables
def index(request):
    session = DBSession()
    category = request.params.get('category')
    current_query = dict()
    page = request.params.get('p')
    posts = session.query(Post).order_by(desc(Post.timestamp))
    if page:
        current_query['p'] = page
    if category:
        posts = posts.filter(Category.name==category)
        current_query['category'] = category
    tag = request.params.get('tag')
    if tag:
        posts = posts.filter(Tag.name==tag)
        current_query['tag'] = tag
    #for entry in posts:
    #    f = StringIO.StringIO()
    #    content = publish_parts(entry.content, writer_name='html')['html_body']
    #    content = content.replace('literal-block', 'literal-block prettyprint')
    #    #entry.shortcontent = BlogHTMLParser().blogfeed(content, f, 5)
    #    entry.shortcontent = content
    #    entries.append(entry)
    return dict(recent_posts=posts, current_query=current_query, p=(page or 1))

@view_config(route_name='entry', renderer='blog:templates/entry.mako')
@sidebar_variables
def entry(request):
    id = request.matchdict['kword_or_id']
    session = DBSession()
    entry = session.query(Post).get(id)
    posts = session.query(Post)
    entry.click_counter += 1
    session.flush()
    #f = StringIO.StringIO()
    #content = BlogHTMLParser().blogfeed(content, f, 2)
    return dict(entry=entry)

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

    def blogfeed(self, data, fileobj, paragraph_num=1, wordcount=200):
        self.paragraph_num, self.wordcount = paragraph_num, wordcount
        self.counter = 0
        self.f = fileobj
        self.anchor_tag = False
        self.feed(data)
        document = self.f.getvalue()
#        document = re.sub(r'\n*<a', ' <a', document)
#        document = re.sub(r'a>\n*', 'a> ', document)
        def repl(matchobj):
            atag = matchobj.group()
            return atag.replace('\n', ' ')
        document = re.sub(r'\n*<a[\d\D]+(a>\n+)?', repl, document)
        print repr(document)
        short_document = '<div class="document"><p>%s</p></div>' % document.replace('\n', '<br>')
        return short_document

    def handle_starttag(self, tag, attrs):
        if self.counter == self.paragraph_num and len(self.f.getvalue()) > self.wordcount:
            return
        html = '<%s %s>'
        s_attrs = ''
        for k,v in attrs:
            s_attrs += ' %s="%s"'%(k,v)
        if tag.strip() == 'a':
            html = html % (tag, s_attrs)
            print >>self.f, html.replace('\n', '').strip()
            self.anchor_tag = True

    def handle_data(self, data):
        if self.counter == self.paragraph_num and len(self.f.getvalue()) > self.wordcount:
            return
        if data.strip() == '':
            return
        if self.anchor_tag:
            self.f.write(data.replace('\n', ' '))
        else:
            print >>self.f, data

    def handle_endtag(self, tag):
        if self.counter == self.paragraph_num and len(self.f.getvalue()) > self.wordcount:
            return
        if tag.strip() == 'a':
            print >>self.f, ('</%s>'%tag).replace('\n', '').strip()
        self.counter += 1
