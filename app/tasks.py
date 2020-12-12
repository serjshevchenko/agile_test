import asyncio
import logging

from aiohttp import web

from app.bl.images import store_all_images

log = logging.getLogger(__name__)


async def schedule_periodic_tasks(app: web.Application) -> None:
    scheduler = app['scheduler']
    scheduler_conf = app['config']['scheduler']

    scheduler.add_job(
        rebuild_image_cache,
        trigger='cron',
        hour='*/1',
        args=[app]
    )
    scheduler.add_job(
        rebuild_image_cache,
        args=[app]
    )


async def rebuild_image_cache(app: web.Application) -> None:
    asyncio.create_task(store_all_images(app))
