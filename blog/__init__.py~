from pyramid.config import Configurator
from pyramid.events import NewRequest, subscriber
from sqlalchemy import engine_from_config

from blog.models import initialize_sql

@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    settings['mako.directories'] = ['blog:templates']
    config = Configurator(settings=settings)
    config.add_static_view('static', 'blog:static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('entry', '/{year}/{month}/{kword_or_id}')
    config.add_route('post', '/post')
    config.scan()
    return config.make_wsgi_app()

