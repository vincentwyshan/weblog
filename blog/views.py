#coding=utf8

import re
import time
import datetime
import StringIO
from hashlib import md5

from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPUnauthorized
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy import desc

import PyRSS2Gen

from blog.models import DBSession
from blog.models import Post, Tag, Category

from docutils.core import publish_parts

import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

_USER = {'vincent' : 'v1984913'}

#@view_config(route_name='test')
def test(request):
    import os
    html = open(os.path.join(os.path.dirname(__file__), 'templates/test.html')).read()
    response = Response(html)
    return response

def _auth(func):
    def _warper(*kargs, **kwarg):
        request = kargs[1] #TODO here might be a pyramid bug
        auth_str = request.headers.get('Authorization')
        if 'Authorization' not in request.headers or not digest_http_auth_valid(auth_str, request.method):
            html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                 "http://www.w3.org/TR/1999/REC-html401-19991224/loose.dtd">
                <HTML>
                  <HEAD>
                    <TITLE>Error</TITLE>
                    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=ISO-8859-1">
                  </HEAD>
                  <BODY><H1>401 Unauthorized.</H1></BODY>
                </HTML>'''
            response = Response(html)
            response.status_int = 401
            #response.headerlist.append(('WWW-Authenticate', 'Basic realm="Secure Area"'))
            tokens = digest_http_auth_tokens()
            tokens['nonce'] = md5(request.remote_addr).hexdigest()
            auth_str = 'Digest '+','.join(['%s="%s"' % (k,v) for k,v in tokens.items()])
            response.headerlist.append(('WWW-Authenticate', auth_str))
        else:
            response = func(request)
        return response
    return _warper

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
        response_dict['header_repl'] = header_repl
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
        posts = posts.join(Post.category).filter(Category.name==category)
        current_query['category'] = category
    tag = request.params.get('tag')
    if tag:
        posts = posts.join(Post.tags).filter(Tag.name==tag)
        current_query['tag'] = tag
    #for entry in posts:
    #    f = StringIO.StringIO()
    #    content = publish_parts(entry.content, writer_name='html')['html_body']
    #    content = content.replace('literal-block', 'literal-block prettyprint')
    #    #entry.shortcontent = BlogHTMLParser().blogfeed(content, f, 5)
    #    entry.shortcontent = content
    #    entries.append(entry)
    return dict(posts=posts, current_query=current_query, p=(page or 1))

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
@_auth
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

@view_config(route_name='delete')
@_auth
def delete(request):
    pid = request.params.get('post')
    category = request.params.get('category')
    tag = request.params.get('tag')
    session = DBSession()
    if pid:
        p = session.query(Post).get(pid)
        session.delete(p)
    if category:
        category = session.query(Category).filter_by(name=category).first()
        for p in category.posts:
            p.category = None
        session.delete(category)
    if tag:
        tag = session.query(Tag).filter_by(name=tag).first()
        tid = tag.id
        session.delete(tag)
        session.bind.execute("delete from rel_post_tag where tag_id=%s" % tid)
    session.flush()
    return Response('1')

def _rss_item(host, post):
    pubdate = datetime.datetime.fromtimestamp(post.timestamp)
    html = publish_parts(post.content, writer_name='html')['html_body']
    des = BlogHTMLParser().blogfeed(html, StringIO.StringIO(), 5)
    return PyRSS2Gen.RSSItem(
            title = post.title,
            link = "http://%s/%s/%s/%s" % (host, pubdate.year, pubdate.month, post.id),
            description = des,
            guid = PyRSS2Gen.Guid("http://%s/%s"%(host,str(post.timestamp))),
            pubDate = pubdate,
            )

@view_config(route_name='rss')
def rss(request):
    host = request.host
    session = DBSession()
    posts = session.query(Post).order_by(desc(Post.timestamp))[:20]
    rss = PyRSS2Gen.RSS2(
            title = "Vincent's Blog feed",
            link = host,
            description = "about my thought, work, programing",
            lastBuildDate = datetime.datetime.utcnow(), 
            items = [_rss_item(host,p) for p in posts]
            )
    f = StringIO.StringIO()
    rss.write_xml(f)
    return Response(f.getvalue())
                

from HTMLParser import HTMLParser
class BlogHTMLParser(HTMLParser):

    def blogfeed(self, data, fileobj, paragraph_num=1):
        self.paragraph_num  = paragraph_num
        self.counter = 0
        self.f = fileobj
        self.anchor_tag = False
        self.feed(data)
        document = self.f.getvalue()
#        document = re.sub(r'\n*<a', ' <a', document)
#        document = re.sub(r'a>\n*', 'a> ', document)
        #def repl(matchobj):
        #    atag = matchobj.group()
        #    return atag.replace('\n', ' ')
        #document = re.sub(r'\n*<a[\d\D]+(a>\n+)?', repl, document)
        #print repr(document)
        #short_document = '<div class="document"><p>%s</p></div>' % document.replace('\n', '<br>')
        #return short_document
        return document

    def handle_starttag(self, tag, attrs):
        if self.counter == self.paragraph_num:
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
        if self.counter == self.paragraph_num:
            return
        if data.strip() == '':
            return
        if self.anchor_tag:
            self.f.write(data.replace('\n', ' '))
        else:
            print >>self.f, data

    def handle_endtag(self, tag):
        if self.counter == self.paragraph_num:
            return
        if tag.strip() == 'a':
            print >>self.f, ('</%s>'%tag).replace('\n', '').strip()
        self.counter += 1

def digest_http_auth_tokens():
    realm = 'loglogvincent Auth'
    qop = 'auth'
    nonce = None
    opaque = '1053267b-17a6-414e-9a75-c61b66f445bb'
    return locals()

def digest_http_auth_parse(auth_str):
    auth_str = auth_str.replace('Digest', '')
    token_list = auth_str.split(',')
    result = {}
    for t in token_list:
        m = re.search('\s*(?P<name>[^=]+)=(?P<val>.+)', t)
        val = m.group('val').strip()
        if val[0] == val[-1] and val[0] in('"', "'"):
            val = val[1:-1]
        result[m.group('name')] = val
    return result

def digest_http_auth_valid(auth_str, method):
    """response=MD5(HA1:nonce:nonceCount:clientNonce:qop:HA2)
    HA1=MD5(username:realm:password)
    HA2=MD5(method:digestURI)
    refreence: http://en.wikipedia.org/wiki/Digest_access_authentication
    """
    data = digest_http_auth_parse(auth_str)
    data.update({'password':_USER[data['username']]})
    HA1 = md5('%(username)s:%(realm)s:%(password)s'%data)
    HA2 = md5('%s:%s' % (method, data['uri']))
    data.update(dict(HA1=HA1.hexdigest(),HA2=HA2.hexdigest()))
    response = md5('%(HA1)s:%(nonce)s:%(nc)s:%(cnonce)s:%(qop)s:%(HA2)s' % data).hexdigest()
    return response == data['response']

def header_repl(content):
    for i in range(1, 4):
        s,t = 'h%s' % i, 'h%s' % (i+1)
        content = content.replace('<'+s, '<'+t)
        content = content.replace(s+'>', t+'>')
    return content.replace('literal-block', 'literal-block prettyprint linenums')
