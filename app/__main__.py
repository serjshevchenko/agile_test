import logging

from aiohttp import web

from .app import create_app


log = logging.getLogger(__name__)


if __name__ == '__main__':
    # todo: init logging
    app = create_app()
    app_config = app['config']['app']
    web.run_app(app, host=app_config['host'], port=app_config['port'])
