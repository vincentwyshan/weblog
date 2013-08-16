#coding=utf8

import os
import re
import time
import StringIO
import datetime
import ConfigParser
from hashlib import md5

from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import (
        HTTPFound,
        HTTPNotFound, 
        HTTPUnauthorized,
)

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc, asc
from beaker.cache import cache_region

from docutils.core import publish_parts
import PyRSS2Gen

from weblog.football import month_name
from weblog.models import (
        DBSession,
        Post,
        Tag,
)




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


def recent_posts():
    "return recent 5 posts."
    session = DBSession()
    posts = session.query(Post).order_by(desc(Post.timestamp))
    posts = posts.slice(0, 5)
    result = []
    for p in posts:
        p.url = p.url_kword or unicode(p.id)
        p.content_title = p.title or _title_from_content(p.content)
        result.append(p)
    return result

@cache_region('default_term', 'index')
def blog_index(page):
    print '\n\nCALL ME\n'
    posts_1page = 9
    session = DBSession()
    posts = session.query(Post).order_by(desc(Post.timestamp))
    _posts = []
    for post in posts[page*posts_1page:(page+1)*posts_1page]:
        post.content_title = post.title or _title_from_content(post.content)
        post.summary_html = publish_parts(post.summary, writer_name='html')['html_body']
        post.url = post.url_kword or unicode(post.id)
        _posts.append(post)
    return {'posts':_posts, 'page_num':page, 'max_page_num':posts.count()/posts_1page, 'recent_posts':recent_posts()}

@view_config(route_name='blog_home', renderer='weblog:templates/blog_home.mako')
def view_index(request):
    page = int(request.GET.get('page', 0))
    return blog_index(page)

@cache_region('default_term', 'archive')
def blog_archive():
    session = DBSession()
    posts = session.query(Post).order_by(desc(Post.id))

    title = u"ARCHIVES"
    post_by_year = []
    for post in posts:
        post.url = post.url_kword or unicode(post.id)
        if not post_by_year or (post.date.year != post_by_year[-1][0]):
            post_by_year.append([post.date.year, [post]])
        else:
            post_by_year[-1][1].append(post)
    return dict(post_by_year=post_by_year, recent_posts=recent_posts(), month_name=month_name, title=title)

@view_config(route_name="blog_archive", renderer="weblog:templates/blog_archive.mako")
def view_archive(request):
    return blog_archive()

@cache_region('default_term', 'tag')
def blog_tag(tag_name):
    session = DBSession()
    tag = session.query(Tag).filter(Tag.name==tag_name)[0]
    posts = session.query(Post).filter(Post.tags.contains(tag)).order_by(desc(Post.date))

    title = u"Tag: %s" % tag_name
    post_by_year = []
    for post in posts:
        post.url = post.url_kword or unicode(post.id)
        if not post_by_year or (post.date.year != post_by_year[-1][0]):
            post_by_year.append([post.date.year, [post]])
        else:
            post_by_year[-1][1].append(post)
    return dict(post_by_year=post_by_year, recent_posts=recent_posts(), month_name=month_name, title=title)

@view_config(route_name="blog_tag", renderer="weblog:templates/blog_archive.mako")
def view_tag(request):
    tag_name = request.matchdict['tag_name'].strip()
    return blog_tag(tag_name)

@cache_region('default_term', 'post')
def blog_post(kword_or_id):
    session = DBSession()
    post = session.query(Post).filter(Post.url_kword==kword_or_id).first()
    if not post and kword_or_id.isdigit():
        post = session.query(Post).get(int(kword_or_id))
    if not post:
        raise HTTPNotFound
    post.content_title = post.title or _title_from_content(post.content)
    parts = publish_parts(post.content, writer_name='html')

    html_body = parts['html_body']
    
    prev_post = session.query(Post).filter(Post.id<post.id).order_by(desc(Post.id))
    if prev_post.count() > 0:
        prev_post = prev_post[0]
        prev_post.content_title = prev_post.title or _title_from_content(prev_post.content)
    else:
        prev_post = None

    next_post = session.query(Post).filter(Post.id>post.id).order_by(asc(Post.id))
    if next_post.count() > 0:
        next_post = next_post[0]
        next_post.content_title = next_post.title or _title_from_content(next_post.content)
    else:
        next_post = None

    post.html_content = html_body
    return {'post':post, 'recent_posts':recent_posts(),
            'prev_post': prev_post, 'next_post':next_post}


@view_config(route_name='blog_post', renderer='weblog:templates/blog_post.mako')
def view_post(request):
    kword_or_id = request.matchdict['kword_or_id'].strip()
    return blog_post(kword_or_id)


@cache_region('long_term', 'rss')
def rss(host):
    session = DBSession()
    posts = session.query(Post).order_by(desc(Post.timestamp))[:20]
    rss = PyRSS2Gen.RSS2(
            title = "Vincent's Blog feed",
            link = host,
            description = "Vincent's work, life ...",
            lastBuildDate = datetime.datetime.utcnow(), 
            items = [_rss_item(host,p) for p in posts]
            )
    f = StringIO.StringIO()
    rss.write_xml(f, encoding='utf8')
    response = Response(f.getvalue())
    response.content_type = "application/rss+xml"
    return response

@view_config(route_name='blog_rss')
def view_rss(request):
    host = request.host
    return rss(host)

@cache_region('default_term', 'about')
def about():
    description='''
    <p>I'm vincent, software engineer at <a href="http://www.capitalvue.com" target="_blank">Capitalvue</a>.</p>
    <p>I use<a href="http://www.python.org" target="_blank">Python</a> for over 5 years.</p>
    <p>I like all about: "open source", "linux", "python", "web development", "reading". </p>
    <p>Now I'm focus on "data-mining", "machine learning", "financial engineering". </p> 



    '''
    return {'description':description, 'recent_posts':recent_posts()}

@view_config(route_name='blog_about', renderer="weblog:templates/blog_about.mako")
def view_about(request):
    return about()


@view_config(route_name='blog_insert_update', renderer='weblog:templates/blog_update.mako')
@_auth
def post(request):
    id = request.params.get('id')
    session = DBSession()
    if request.method == 'POST':
        title, content = request.POST['title'], request.POST['content']
        tags = request.POST['tags']
        summary = request.POST['summary']
        url_kword = request.POST['url_kword']
        assert title not in ('', None), "Missing title"
        assert url_kword not in ('', None), "Missing url_kword"
        assert content not in ('', None), "Missing content"
        p = None
        if id:
            p = session.query(Post).get(id)
        else:
            p = Post(timestamp=time.time(), date=datetime.date.today())
            session.add(p)
        p.title = title
        p.content = content
        p.summary = summary
        p.url_kword = url_kword
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
        return HTTPFound(location=request.route_url('blog_home'))
    else:
        entry = None
        if id:
            entry = session.query(Post).get(id)
        start = entry.id-2 if entry else 0
        entries=session.query(Post).filter(Post.id>=start).limit(5)
        return dict(entry=entry, entries=entries, recent_posts=recent_posts())

@view_config(route_name='blog_delete')
@_auth
def delete(request):
    pid = request.params.get('post_id')
    if pid:
        session = DBSession()
        p = session.query(Post).get(pid)
        session.delete(p)
        session.flush()
    else:
        return Response("Not find")
    return Response('Delete done!')

def _rss_item(host, post):
    pubdate = datetime.datetime.fromtimestamp(post.timestamp)
    html = publish_parts(post.content, writer_name='html')['html_body']
    link = "http://%s/post/%s" % (host, post.url_kword or post.id)
    return PyRSS2Gen.RSSItem(
            title = post.title,
            link = link,
            description = html,
            guid = link,#PyRSS2Gen.Guid("http://%s/%s"%(host,str(post.timestamp))),
            pubDate = pubdate,
            )

def _title_from_content(content):
    content = content.strip().lstrip('-').lstrip('=').lstrip('~').lstrip('_').strip()
    title = content.split('\n')[0]
    return title

def _summary_from_content(content):
    #TODO summary from restructure text
    return content


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

_USER = {}
def _loadusers(users):
    cfg = ConfigParser.ConfigParser()
    path = os.path.join(os.path.dirname(__file__), 'users.cfg')
    cfg.read(path)
    for user, passwd in cfg.items('users'):
        users[user] = passwd
_loadusers(_USER)

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


