#coding=utf8

import urllib

import transaction
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy import desc
from sqlalchemy import func
from docutils.core import publish_parts

from weblog.security import auth
from weblog.models import (
    DBSession,
    Post, Tag, rel_post_tag
)


@view_config(route_name='home', renderer='templates/home.html')
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

        return {'posts': posts, 'title': u"Vincent's footprint", 'pagi': pagi}


@view_config(route_name="post", renderer="templates/post.html")
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

        return {'post': post, 'title': post.title, 'post_content': html_body}


@view_config(route_name="tags", renderer="templates/tags.html")
def tags(request):
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

    return {'tags': _tags, 'title': u"Tags | VINCNET'S FOOTPRINT"}


@view_config(route_name="tag_posts", renderer="templates/tags_detail.html")
def tags_detail(request):
    tag_name = request.matchdict['name'].strip()
    tag = DBSession.query(Tag).filter_by(name=tag_name).first()
    if not tag:
        return HTTPNotFound("")

    posts = list(tag.posts)
    del posts

    return {'tag': tag, 'title': u"Tag: %s" % tag.name}


@view_config(route_name="about", renderer="templates/about.html")
def about(request):
    return dict(title="About | VINCENT'S FOOTPRINT")


@view_config(route_name="edit", renderer="templates/edit.html")
@view_config(route_name="add", renderer="templates/edit.html")
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
                post = Post()
                DBSession.add(post)
            post.title = post_title
            post.url_kword = url_kword
            post.summary = summary
            post.content = content

            new_tags = []
            for name in tags.split(','):
                name = name.strip()
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
