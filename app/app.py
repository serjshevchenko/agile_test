import asyncio
import typing as t

from aiohttp import web

from app import signals
from app.config import get_config
from app.routes import setup_routes
from app.tasks import schedule_periodic_tasks


def create_app(loop: t.Optional[asyncio.AbstractEventLoop] = None) -> web.Application:
    loop = loop or asyncio.get_event_loop()
    config = get_config()
    app = web.Application(loop=loop)
    app['loop'] = loop
    app['config'] = config

    # Setup signals
    # To run on app startup
    app.on_startup.extend([
        signals.init_client_session,
        signals.connect_redis,
        signals.configure_scheduler,
        schedule_periodic_tasks,
    ])

    # To run before shutdown
    app.on_cleanup.extend([
        signals.destroy_client_session,
        signals.disconnect_redis,
        signals.shutdown_scheduler,
    ])

    # Routes
    setup_routes(app)

    return app
