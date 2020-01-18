from pyramid.config import Configurator
from . import database
from . import routes


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Template
    config.include("pyramid_mako")
    config.add_mako_renderer(".html")

    # i18n
    from weblog.common import _t

    config.add_request_method(_t, "_")
    config.add_translation_dirs("weblog:locale")

    config.include(database)
    config.include(routes)

    config.scan()
    return config.make_wsgi_app()
