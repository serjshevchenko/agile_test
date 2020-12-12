import logging

import pytz
from aiohttp import ClientSession, web
from aioredis import create_redis_pool
from apscheduler.schedulers.asyncio import AsyncIOScheduler

log = logging.getLogger(__name__)


async def init_client_session(app: web.Application) -> None:
    app['session'] = ClientSession()
    log.info('ClientSession initialized')


async def destroy_client_session(app: web.Application) -> None:
    session = app['session']
    await session.close()
    log.info('ClientSession closed')


async def connect_redis(app: web.Application) -> None:
    conf = app['config']['redis']
    conn = await create_redis_pool(
        (conf['host'], conf['port']),
        db=conf['db'],
        loop=app['loop']
    )
    app['redis'] = conn
    log.info('Redis connected')


async def disconnect_redis(app: web.Application) -> None:
    app['redis'].close()
    await app['redis'].wait_closed()
    log.info('Redis disconnected')


async def configure_scheduler(app: web.Application) -> None:
    job_defaults = {
        'coalesce': True,
    }
    scheduler = AsyncIOScheduler(
        job_defaults=job_defaults,
        timezone=pytz.timezone('Europe/Kiev'),
    )
    app['scheduler'] = scheduler

    # Setup debug logging
    app_config = app['config']['app']
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.start()
    log.info('APScheduler started')


async def shutdown_scheduler(app: web.Application) -> None:
    app['scheduler'].shutdown(wait=False)
    log.info('APScheduler stopped')
