"""
1. walk through all index
2. load all posts
3. record inserted or updated posts' id in a list
4. remove post not in the list
5. remove empty tags
"""

import re
import os
import datetime
import logging
from typing import Dict

import click
import transaction
from yaml import load as load_yml
from dateutil.parser import parse as date_parse
from docutils.core import publish_parts

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


from pyramid.paster import (
    get_appsettings,
    setup_logging,
)


from weblog.common import thumbnail, img_static
from ..database.meta import Base
from ..database import (
    get_engine,
    get_session_factory,
    get_tm_session,
    Post,
    Tag,
)

log: logging.Logger = None


@click.command(
    __name__, context_settings=dict(help_option_names=["-h", "--help"])
)
@click.option(
    "--config", "-c", type=str, required=True, help="config file path"
)
def main(config):
    setup_logging(config)
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    settings = get_appsettings(config_uri=config, options={})

    engine = get_engine(settings, "sqlalchemy.")
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)

    posts_root = settings["posts_root"]
    post_files = get_post_files(posts_root)

    post_ids = set()
    tag_ids = set()

    for index_yml in get_index_files(posts_root):
        with transaction.manager:
            _post_ids, _tag_ids = load_yml_index(
                session, index_yml, post_files
            )
            post_ids.update(_post_ids)
            tag_ids.update(_tag_ids)

    with transaction.manager:
        session.query(Tag).filter(Tag.id.notin_(list(tag_ids))).delete(
            synchronize_session=False
        )
        session.query(Post).filter(Post.id.notin_(list(post_ids))).delete(
            synchronize_session=False
        )

    process_images(posts_root)


def get_mtime(path):
    mtime = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(mtime)


def process_images(posts_root):
    static_dir = os.path.join(posts_root, "static")

    static_desktop = os.path.join(posts_root, img_static.desktop_dir)
    static_mobile = os.path.join(posts_root, img_static.mobile_dir)
    for _d in (static_desktop, static_mobile):
        if not os.path.isdir(_d):
            os.makedirs(_d)

    for root, dirs, files in os.walk(static_dir):
        for f in files:
            if f.startswith("."):
                continue

            path = os.path.join(root, f)
            path_desktop = path.replace(static_dir, static_desktop)
            if os.path.isfile(path_desktop) and get_mtime(path) <= get_mtime(
                path_desktop
            ):
                continue

            log.info("process image: {}".format(path))
            raw = open(path, "rb").read()
            blob = thumbnail(raw, img_static.desktop_width)
            if not os.path.isdir(os.path.split(path_desktop)[0]):
                os.makedirs(os.path.split(path_desktop)[0])
            open(path_desktop, "wb").write(blob)

            path_mobile = path.replace(static_dir, static_mobile)
            if not os.path.isdir(os.path.split(path_mobile)[0]):
                os.makedirs(os.path.split(path_mobile)[0])
            blob = thumbnail(raw, img_static.mobile_width)
            open(path_mobile, "wb").write(blob)


def load_yml_index(session, index_yml: str, post_files: Dict[str, str]):
    log.info("load yml: {}".format(index_yml))
    data = load_yml(open(index_yml, "r"), Loader=Loader)
    post_ids = set()
    tag_ids = set()

    for url_kw, attrs in data.items():
        title = attrs["title"]
        summary = text_to_html(attrs["summary"])
        tags = [t.strip() for t in attrs["tags"].split(",") if t.strip()]
        created_time = attrs["created"]
        if not isinstance(created_time, (datetime.datetime, datetime.date)):
            created_time = date_parse(created_time)
        if isinstance(created_time, datetime.datetime):
            created_time = created_time.replace(tzinfo=None)


        post = session.query(Post).filter(Post.url_kword == url_kw).first()
        if not post:
            post = Post(url_kword=url_kw)
            session.add(post)

        if post.url_kword != url_kw:
            post.url_kword = url_kw
        if post.title != title:
            post.title = title
        if post.summary != summary:
            post.summary = summary
        if post.created != created_time:
            post.created = created_time

        content = load_post_content(post_files, url_kw)
        if post.content != content:
            post.content = content

        for t in tags:
            tag = session.query(Tag).filter(Tag.name == t).first()
            if not tag:
                tag = Tag(name=t)
                session.add(tag)

            if tag not in post.tags:
                post.tags.append(tag)

        session.flush()

        post_ids.add(post.id)
        if post.tags:
            tag_ids.update([t.id for t in post.tags])

    return post_ids, tag_ids


def load_post_content(post_files, url_kw):
    post_file = post_files[url_kw.lower()]
    file_content = open(post_file, "r").read()
    if post_file.lower().endswith("rst"):
        file_content = re.sub(
            r"[\.\/]*\/static\/", r"/post-static/", file_content
        )
        parts = publish_parts(file_content, writer_name="html")
        content = parts["body"]
    elif post_file.lower().endswith("txt"):
        content = text_to_html(file_content)
    else:
        raise NotImplementedError(
            "can't support format: {}".format(post_file)
        )
    return content


def text_to_html(content):
    parts = [p.strip() for p in content.split("\n") if p.strip()]
    return "".join(["<p>{}</p>".format(p) for p in parts])


def get_index_files(posts_root: str):
    result = []
    for p in os.listdir(os.path.join(posts_root, "index")):
        path = os.path.join(posts_root, "index", p)
        if (
            os.path.isfile(path)
            and p.startswith("index")
            and p.endswith(".yml")
        ):
            result.append(path)

    return result


def get_post_files(posts_root: str):
    root = os.path.join(posts_root, "post")
    result = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            if name.endswith("rst") or name.endswith("txt"):
                url_kw = name.lower()
                url_kw = os.path.splitext(url_kw)[0]
                if url_kw in result:
                    raise Exception("duplicated file name {}".format(name))

                result[url_kw] = os.path.join(dirpath, name)

    return result


if __name__ == "__main__":
    main()
