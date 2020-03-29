import os
import math
import mimetypes
import datetime
import pickle
from typing import Dict
from io import StringIO
from urllib.parse import urlencode

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy import desc

from pyramid.renderers import render_to_response
import PyRSS2Gen

from weblog.cache import cache_view, _IMAGE_DIR
from weblog.common import _, _t, img_static
from weblog.database.models import Post, Tag, rel_post_tag, Image


@view_config(route_name="home")
@cache_view(60)
def home(request):
    posts = request.dbsession.query(Post)
    total = posts.count()

    current = int(request.params.get("p", 1))
    num_per_page = 15
    pagi = Paginator(current, total, num_per_page, p_argname="p")

    posts = posts.order_by(desc(Post.created))
    posts = posts.offset((current - 1) * pagi.num_per_page)
    posts = posts.limit(pagi.num_per_page)

    context = {
        "posts": posts,
        "title": request.registry.settings["site_name"],
        "pagi": pagi,
        "request": request,
    }
    return render_to_response("home.html", context)


@view_config(route_name="post")
@cache_view(60)
def post(request):
    url_kword = request.matchdict["url_kword"]
    dbsession = request.dbsession
    post = dbsession.query(Post).filter_by(url_kword=url_kword).first()

    # load tags
    if not post:
        return HTTPNotFound()

    tags = post.tags
    del tags
    # parts = publish_parts(post.content, writer_name="html")
    # html_body = parts["body"]

    context = {
        "post": post,
        "title": post.title,
        "post_content": post.content,
        "request": request,
    }
    return render_to_response("post.html", context)


@view_config(route_name="tags")
@cache_view(60)
def tags(request):
    dbsession = request.dbsession

    _tags = list(dbsession.query(Tag))
    _tags = {
        t.name: dbsession.query(rel_post_tag).filter_by(tag_id=t.id).count()
        for t in _tags
    }
    _tags = {name: value for name, value in _tags.items() if value > 0}

    max_num = max(_tags.values())
    min_num = min(_tags.values())
    distance = max_num - min_num
    distance = 10 if distance < 10 else distance
    for name, val in _tags.items():
        if distance == 0:
            _tags[name] = 1
            continue
        _tags[name] = 1 + ((val - min_num) * 1.0 / distance)

    context = {
        "tags": _tags,
        "title": u"Tags | {}".format(request.registry.settings["site_name"]),
        "request": request,
    }
    return render_to_response("tags.html", context)


@view_config(route_name="tag_posts")
@cache_view(60)
def tags_detail(request):
    tag_name = request.matchdict["name"].strip()
    tag = request.dbsession.query(Tag).filter_by(name=tag_name).first()
    if not tag:
        return HTTPNotFound("")

    posts = list(tag.posts)
    del posts

    context = {"tag": tag, "title": u"Tag: %s" % tag.name, "request": request}
    return render_to_response("tags_detail.html", context)


@view_config(route_name="about")
@cache_view(60)
def about(request):
    _about = _t(request, _(u"title-about"))
    context = dict(
        title=_about + u" | {}".format(request.registry.settings["site_name"]),
        request=request,
    )
    return render_to_response("about.html", context)


@view_config(route_name="rss")
@cache_view(60)
def rss(request):
    host = request.host
    posts = request.dbsession.query(Post).order_by(desc(Post.id))
    posts = posts.limit(30)
    rss = PyRSS2Gen.RSS2(
        title="{} Feed".format(request.registry.settings["site_name"]),
        link=u"http://" + host,
        description="{} Feed".format(request.registry.settings["site_name"]),
        lastBuildDate=datetime.datetime.utcnow(),
        items=[rss_item(host, p) for p in posts],
    )
    f = StringIO()
    rss.write_xml(f, encoding="utf8")

    response = Response(f.getvalue())
    response.content_type = "application/rss+xml"
    return response


def rss_item(host, post):
    pubdate = post.created
    link = "http://%s/post/%s" % (host, post.url_kword)
    return PyRSS2Gen.RSSItem(
        title=post.title,
        link=link,
        description=post.summary,
        guid=link,  # PyRSS2Gen.Guid("http://%s/%s"%(host,str(post.timestamp)))
        pubDate=pubdate,
    )


@view_config(route_name="post_static")
def post_static(request):
    path = request.matchdict["path"]
    posts_root = request.registry.settings["posts_root"]

    if "mobile" in request.params:
        data = open(
            os.path.join(posts_root, img_static.desktop_dir, path), "rb"
        ).read()
    elif "raw" in request.params:
        data = open(
            os.path.join(posts_root, img_static.raw, path), "rb"
        ).read()
    else:
        data = open(
            os.path.join(posts_root, img_static.desktop_dir, path), "rb"
        ).read()

    response = Response(data)
    response.content_type = mimetypes.guess_type(path)[0] or "image/jpeg"
    response.cache_expires = 3600 * 24 * 365
    return response


@view_config(route_name="resource_img")
def resource_img(request):
    image_name = request.matchdict["img_name"]
    md5 = image_name.split(".")[0]
    file_type = "thumbnail"
    if "raw" in request.params:
        file_type = "raw"

    # cache
    cache_path = os.path.join(_IMAGE_DIR, md5)
    cache_path = (
        cache_path if file_type == "raw" else (cache_path + ".thumbnail")
    )

    filename = None
    data = None

    if os.path.exists(cache_path):
        data: Dict = pickle.load(open(cache_path, "rb"))
        filename = data["filename"]
        data = data["content"]

    if not filename:
        image = request.dbsession.query(Image).filter_by(md5=md5).first()
        if not image:
            return HTTPNotFound("")

        data = image.image_raw if file_type == "raw" else image.image_thumbnail
        filename = "%s.%s" % (image.md5, image.image_ext)

        pickle.dump(
            dict(
                filename=filename,
                content=data,
                timestamp=datetime.datetime.utcnow(),
            ),
            open(cache_path, "wb"),
        )

    response = Response(data)
    response.content_type = (
        mimetypes.guess_type(filename[0])[0] or "image/jpeg"
    )
    # response.content_disposition = 'attachment; filename="%s"' % filename
    response.cache_expires = 3600 * 24 * 365
    return response


@view_config(route_name="language")
def language(request):
    lang = request.params.get("lang")
    next_url = request.referrer or "/"
    if next_url != "/" and request.host not in next_url:
        site_address = request.registry.settings.get("site_address", "/")
        if site_address == "/":
            next_url = request.host
        else:
            next_url = site_address
    response = HTTPFound(next_url)
    if lang == "zh_CN":
        response.set_cookie("_LOCALE_", "zh_CN", max_age=3600 * 24 * 365)
    else:
        response.set_cookie("_LOCALE_", "en", max_age=3600 * 24 * 365)
    return response


class Temp:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Paginator(object):
    _start = 1

    total: int = 0
    num_per_page: int = 30
    current: int
    offset = 3
    paras = {}
    p_argname = "page"

    _prevlist = None
    _nextlist = None
    _page_total = None

    def __init__(
        self,
        current,
        total=None,
        num_per_page=None,
        p_argname=None,
        paras=None,
        offset=None,
    ):
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
                    self.paras[k] = ""

        if self.current > self._start:
            self.show_prevbutton = True
        else:
            self.show_prevbutton = False

        if self.current < self.pages:
            self.show_nextbutton = True
        else:
            self.show_nextbutton = False

        if self.prevlist and self.prevlist[0] != self._start:
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
        self._page_total = math.floor(self.total / self.num_per_page)
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
            if _prev < self._start:
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
        paras = urlencode(paras)
        return paras
