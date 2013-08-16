from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings

from .models import (
    DBSession,
    Base,
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=36000)
    config.add_route('blog_home', '/')

    config.add_route('blog_post', '/post/{kword_or_id}')
    config.add_route('blog_rss', '/rss')
    config.add_route('blog_about', '/about')
    config.add_route('blog_insert_update', '/update')
    config.add_route('blog_delete', '/delete')

    config.add_route('blog_archive', '/archive')
    config.add_route('blog_tag', '/tag/{tag_name}')

    config.scan()
    return config.make_wsgi_app()

