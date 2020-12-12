import logging

from aiohttp import web


log = logging.getLogger(__name__)


async def schedule_periodic_tasks(app: web.Application) -> None:
    scheduler = app['scheduler']
    scheduler_conf = app['config']['scheduler']

    scheduler.add_job(
        rebuild_image_cache,
        'interval',
        hours=scheduler_conf['hour'],
        args=[app]
    )


async def rebuild_image_cache(app: web.Application) -> None:
    redis = app['redis']
