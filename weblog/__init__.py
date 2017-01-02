from pyramid.config import Configurator
from sqlalchemy import engine_from_config

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
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Template
    config.include('pyramid_mako')
    config.add_mako_renderer('.html')

    config.add_route('home', '/')
    config.add_route('post', '/post/{url_kword}')
    config.add_route('tags', '/tags')
    config.add_route('tag_posts', '/tags/{name}')
    config.add_route('about', '/about')

    config.add_route('add', '/edit')
    config.add_route('edit', '/edit/{post_id}')

    config.scan()
    return config.make_wsgi_app()
