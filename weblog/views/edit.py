import hashlib
import os
import shutil

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy import func

from weblog.cache import _ROOTDIR, _IMAGE_DIR
from weblog.common import thumbnail
from weblog.database import Image, Post, Tag
from weblog.security import auth
from weblog.views.blog import Temp


@view_config(route_name="images", renderer="images.html")
@auth
def images(request):
    page_number = int(request.params.get("page", 1))
    page_length = 5
    image_list = request.dbsession.query(Image).order_by(Image.id.desc())
    image_list = image_list.offset((page_number - 1) * page_length)
    image_list = image_list.limit(page_length)
    image_list = list(image_list)
    image_list.reverse()
    return dict(images=image_list, page=page_number, length=page_length)


@view_config(route_name="image_submit")
@auth
def image_submit(request):
    raw = request.POST["image"].file.read()
    filename = request.POST["image"].filename
    md5 = hashlib.md5(raw).hexdigest()
    exists = request.dbsession.query(Image).filter_by(md5=md5).first()
    if exists:
        return HTTPFound("/images")

    image = Image()
    image.md5 = md5
    image.image_ext = filename.split(".")[-1]
    image.image_raw = raw
    image.image_thumbnail = thumbnail(raw)
    request.dbsession.add(image)

    return HTTPFound("/images")


@view_config(route_name="edit", renderer="edit 2.html")
@view_config(route_name="add", renderer="edit 2.html")
@auth
def edit(request):
    dbsession = request.dbsession

    pid = request.matchdict.get("post_id")
    post_title = request.params.get("title")
    url_kword = request.params.get("url_kword")
    tags = request.params.get("tags", "")
    summary = request.params.get("summary", "")
    content = request.params.get("content", "")

    # navigator
    def get_navigator():
        post_prev, post_next = None, None
        if pid:
            post_next = dbsession.query(Post).get(int(pid) + 1)
            post_prev = dbsession.query(Post).get(int(pid) - 1)
        else:
            result = dbsession.query(func.max(Post.id).label("id")).first()
            if result:
                max_id = result.id
                post_prev = dbsession.query(Post).get(max_id)
        return post_prev, post_next

    title = u"$$_CREATE NEW_$$"

    # check data:
    error_msg = ""
    if request.POST:
        try:
            assert post_title not in ("", None), "title"
            assert url_kword not in ("", None), "url_keyword"
            assert summary not in ("", None), "summary"
            assert content not in ("", None), "content"
        except Exception as e:
            error_msg = u"error: missing value for %s" % str(e)
            post = Temp(
                id=pid,
                title=post_title,
                url_kword=url_kword,
                summary=summary,
                content=content,
            )
            post_prev, post_next = get_navigator()
            return locals()

    post = None
    if pid:
        post = dbsession.query(Post).get(pid)
        title = u"Edit %s" % post.title

    if request.POST:
        if not pid:
            post = Post(url_kword=url_kword)
            dbsession.add(post)
        post.title = post_title
        # post.url_kword = url_kword
        post.summary = summary
        post.content = content

        new_tags = []
        for name in tags.split(","):
            name = name.strip()
            if not name:
                continue
            tag = dbsession.query(Tag).filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                dbsession.add(tag)
            new_tags.append(tag)
        for tag in list(post.tags):
            post.tags.remove(tag)
        for tag in new_tags:
            post.tags.append(tag)
        dbsession.flush()
        return HTTPFound("/edit/%s" % post.id)

    if not post:
        post = Temp(
            id=pid,
            title=post_title,
            url_kword=url_kword,
            summary=summary,
            content=content,
            tags=tags,
        )
        post_prev, post_next = get_navigator()
        return locals()

    tags = u",".join([t.name for t in post.tags])
    post_prev, post_next = get_navigator()

    # delete cache
    shutil.rmtree(_ROOTDIR)
    os.makedirs(_ROOTDIR)
    os.makedirs(_IMAGE_DIR)
    return locals()