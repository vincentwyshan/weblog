#coding=utf8

import os
import urllib
import hashlib
import mimetypes
import datetime
import StringIO
import cPickle

import transaction
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy import desc
from sqlalchemy import func
from docutils.core import publish_parts

from pyramid.renderers import render_to_response
import PyRSS2Gen

from weblog.security import auth
from weblog.cache import cache_view, _IMAGE_DIR
from weblog.common import thumbnail, _, _t
from weblog.models import (
    DBSession,
    Post, Tag, rel_post_tag, Image
)


@view_config(route_name='home')
@cache_view(60)
def home(request):
    with transaction.manager:
        posts = DBSession.query(Post)

        current = int(request.params.get('p', 1))
        total = posts.count()
        num_per_page = 15
        pagi = Paginator(current, total, num_per_page, p_argname='p')

        posts = posts.order_by(desc(Post.created))
        posts = posts.offset((current-1) * pagi.num_per_page)
        posts = posts.limit(pagi.num_per_page)

        context = {
            'posts': posts, 'title': u"VINCENT'S FOOTPRINT", 'pagi': pagi,
            'request': request
        }
        return render_to_response("templates/home.html", context)


@view_config(route_name="post")
@cache_view(60)
def post(request):
    with transaction.manager:
        url_kword = request.matchdict['url_kword']
        post = DBSession.query(Post).filter_by(url_kword=url_kword).first()

        # load tags
        if not post:
            return HTTPNotFound()

        tags = post.tags
        del tags
        parts = publish_parts(post.content, writer_name='html')
        html_body = parts['body']

        context = {
            'post': post, 'title': post.title, 'post_content': html_body,
            'request': request
        }
        return render_to_response("templates/post.html", context)


@view_config(route_name="tags")
@cache_view(60)
def tags(request):
    with transaction.manager:
        _tags = list(DBSession.query(Tag))
        _tags = {
            t.name: DBSession.query(rel_post_tag).filter_by(tag_id=t.id).count()
            for t in _tags
        }
        _tags = {
            name: value for name, value in _tags.items() if value > 0
        }

        max_num = max(_tags.values())
        min_num = min(_tags.values())
        distance = max_num - min_num
        distance = 10 if distance < 10 else distance
        for name, val in _tags.items():
            if distance == 0:
                _tags[name] = 1
                continue
            _tags[name] = 1 + ((val - min_num)*1.0 / distance)

        context = {
            'tags': _tags, 'title': u"Tags | VINCNET'S FOOTPRINT",
            'request': request
        }
    return render_to_response("templates/tags.html", context)


@view_config(route_name="tag_posts")
@cache_view(60)
def tags_detail(request):
    with transaction.manager:
        tag_name = request.matchdict['name'].strip()
        tag = DBSession.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            return HTTPNotFound("")

        posts = list(tag.posts)
        del posts

        context = {'tag': tag, 'title': u"Tag: %s" % tag.name, 'request': request}
    return render_to_response("templates/tags_detail.html", context)


@view_config(route_name="about")
@cache_view(60)
def about(request):
    _about = _t(request, _(u"About"))
    context = dict(title=_about + u" | VINCENT'S FOOTPRINT",
                   request=request)
    return render_to_response("templates/about.html", context)


@view_config(route_name="rss")
@cache_view(60)
def rss(request):
    with transaction.manager:
        host = request.host
        posts = DBSession.query(Post).order_by(desc(Post.id))
        posts = posts.limit(30)
        rss = PyRSS2Gen.RSS2(title="VINCENTSFOOTPRINT Blog Feed",
                             link=u'http://' + host,
                             description="VINCENTSFOOTPRINT Blog Feed",
                             lastBuildDate=datetime.datetime.utcnow(),
                             items=[rss_item(host, p) for p in posts]
                             )
        f = StringIO.StringIO()
        rss.write_xml(f, encoding='utf8')
    response = Response(f.getvalue())
    response.content_type = "application/rss+xml"
    return response


def rss_item(host, post):
    pubdate = post.created
    html = publish_parts(post.content, writer_name='html')['html_body']
    link = "http://%s/post/%s" % (host, post.url_kword)
    return PyRSS2Gen.RSSItem(
            title=post.title,
            link=link,
            description=html,
            guid=link,#PyRSS2Gen.Guid("http://%s/%s"%(host,str(post.timestamp))),
            pubDate=pubdate,
            )


@view_config(route_name="images", renderer="templates/images.html")
@auth
def images(request):
    with transaction.manager:
        page_number = int(request.params.get('page', 1))
        page_length = 5
        image_list = DBSession.query(Image).order_by(Image.id.desc())
        image_list = image_list.offset((page_number-1) * page_length)
        image_list = image_list.limit(page_length)
        image_list = list(image_list)
        image_list.reverse()
        return dict(images=image_list, page=page_number, length=page_length)


@view_config(route_name="image_submit")
@auth
def image_submit(request):
    with transaction.manager:
        raw = request.POST['image'].file.read()
        filename = request.POST['image'].filename
        md5 = hashlib.md5(raw).hexdigest()
        exists = DBSession.query(Image).filter_by(md5=md5).first()
        if exists:
            return HTTPFound('/images')

        image = Image()
        image.md5 = md5
        image.image_ext = filename.split('.')[-1]
        image.image_raw = raw
        image.image_thumbnail = thumbnail(raw)
        DBSession.add(image)

        return HTTPFound('/images')


@view_config(route_name="resource_img")
def resource_img(request):
    image_name = request.matchdict['img_name']
    md5 = image_name.split('.')[0]
    file_type = 'thumbnail'
    if 'raw' in request.params:
        file_type = 'raw'

    # cache
    cache_path = os.path.join(_IMAGE_DIR, md5)
    cache_path = (
        cache_path if file_type == 'raw' else (cache_path + '.thumbnail')
    )
    if os.path.exists(cache_path):
        data = open(cache_path, 'rb').read()
        filename, data = data.split('|||||')
    else:
        with transaction.manager:
            image = DBSession.query(Image).filter_by(md5=md5).first()
            if not image:
                return HTTPNotFound("")
            data = (
                image.image_raw if file_type == 'raw' else image.image_thumbnail
            )
            filename = '%s.%s' % (image.md5, image.image_ext)
            data = str(filename) + '|||||' + data
            open(cache_path, 'wb').write(data)
    response = Response(data)
    response.content_type = (
        mimetypes.guess_type(filename[0])[0] or 'image/jpeg'
    )
    # response.content_disposition = 'attachment; filename="%s"' % filename
    response.cache_expires = 3600*24*365
    return response


@view_config(route_name="edit", renderer="templates/edit 2.html")
@view_config(route_name="add", renderer="templates/edit 2.html")
@auth
def edit(request):
    with transaction.manager:
        pid = request.matchdict.get('post_id')
        post_title = request.params.get('title')
        url_kword = request.params.get('url_kword')
        tags = request.params.get('tags', '')
        summary = request.params.get('summary', '')
        content = request.params.get('content', '')

        # navigator
        def get_navigator():
            post_prev, post_next = None, None
            if pid:
                post_next = DBSession.query(Post).get(int(pid) + 1)
                post_prev = DBSession.query(Post).get(int(pid) - 1)
            else:
                result = DBSession.query(func.max(Post.id).label('id')).first()
                if result:
                    max_id = result.id
                    post_prev = DBSession.query(Post).get(max_id)
            return post_prev, post_next

        title = u"$$_CREATE NEW_$$"

        # check data:
        error_msg = ''
        if request.POST:
            try:
                assert post_title not in ('', None), 'title'
                assert url_kword not in ('', None), 'url_keyword'
                assert summary not in ('', None), 'summary'
                assert content not in ('', None), 'content'
            except Exception as e:
                error_msg = u"error: missing value for %s" % str(e)
                post = Temp(id=pid, title=post_title, url_kword=url_kword,
                            summary=summary, content=content)
                post_prev, post_next = get_navigator()
                return locals()

        post = None
        if pid:
            post = DBSession.query(Post).get(pid)
            title = u"Edit %s" % post.title

        if request.POST:
            if not pid:
                post = Post(url_kword=url_kword)
                DBSession.add(post)
            post.title = post_title
            # post.url_kword = url_kword
            post.summary = summary
            post.content = content

            new_tags = []
            for name in tags.split(','):
                name = name.strip()
                if not name:
                    continue
                tag = DBSession.query(Tag).filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    DBSession.add(tag)
                new_tags.append(tag)
            for tag in list(post.tags):
                post.tags.remove(tag)
            for tag in new_tags:
                post.tags.append(tag)
            DBSession.flush()
            return HTTPFound("/edit/%s" % post.id)

        if not post:
            post = Temp(id=pid, title=post_title, url_kword=url_kword,
                        summary=summary, content=content, tags=tags)
            post_prev, post_next = get_navigator()
            return locals()

        tags = u','.join([t.name for t in post.tags])
        post_prev, post_next = get_navigator()
        return locals()


@view_config(route_name='language')
def language(request):
    lang = request.params.get('lang')
    response = HTTPFound(request.referrer or '/')
    if lang == 'zh_CN':
        response.set_cookie('_LOCALE_', 'zh_CN', max_age=3600*24*365)
    else:
        response.set_cookie('_LOCALE_', 'en', max_age=3600*24*365)
    return response


class Temp:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Paginator(object):
    total = 0
    num_per_page = 30
    current = 0
    offset = 3
    paras = {}
    p_argname = 'page'

    _prevlist = None
    _nextlist = None
    _page_total = None

    def __init__(self, current, total=None, num_per_page=None, p_argname=None,
                 paras=None, offset=None):
        """
        :param current: current page number, start from 1
        :param p_argname: pagination parameter name
        :param paras: other parameters, dictionary
        :param offset: show how many page numbers before and after current page
        """
        if total:
            self.total = total
        if num_per_page:
            self.num_per_page = num_per_page
        if current:
            self.current = current
        if p_argname:
            self.p_argname = p_argname
        if offset:
            self.offset = offset
        if paras:
            self.paras = paras
            for k, v in self.paras.items():
                assert isinstance(k, str)
                if not v:
                    self.paras[k] = ''
                if isinstance(v, unicode):
                    self.paras[k] = v.encode('utf8')

        if self.current > 1:
            self.show_prevbutton = True
        else:
            self.show_prevbutton = False

        if self.current < self.pages:
            self.show_nextbutton = True
        else:
            self.show_nextbutton = False

        if self.prevlist and self.prevlist[0] != 1:
            self.show_firstpage = True
        else:
            self.show_firstpage = False

        if self.nextlist and self.nextlist[-1] < self.pages:
            self.show_lastpage = True
        else:
            self.show_lastpage = False

    @property
    def pages(self):
        """total page number."""
        if self._page_total is not None:
            return self._page_total
        self._page_total = (self.total / self.num_per_page)
        if self.total % self.num_per_page != 0:
            self._page_total += 1
        return self._page_total

    @property
    def prevlist(self):
        """start number is 1"""
        if self._prevlist is not None:
            return self._prevlist

        self._prevlist = []
        _prev = self.current
        while len(self._prevlist) < self.offset:
            _prev -= 1
            if _prev < 1:
                break
            self._prevlist.insert(0, _prev)
        return self._prevlist

    @property
    def nextlist(self):
        """start number is 1"""
        if self._nextlist is not None:
            return self._nextlist

        self._nextlist = []
        _next = self.current
        while len(self._nextlist) < self.offset:
            _next += 1
            if _next > self.pages:
                break
            self._nextlist.append(_next)
        return self._nextlist

    def param(self, page, kwarg={}):
        """
        encode url parameters with given `page` number.
        """
        paras = {}
        paras.update(self.paras)
        paras.update(kwarg)
        paras[self.p_argname] = page
        paras = urllib.urlencode(paras)
        return paras
