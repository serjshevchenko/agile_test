import logging

from aiohttp import web

from .app import create_app
from .logger import configure_logging

log = logging.getLogger(__name__)


if __name__ == '__main__':
    configure_logging()
    app = create_app()
    app_config = app['config']['app']
    web.run_app(app, host=app_config['host'], port=app_config['port'])
