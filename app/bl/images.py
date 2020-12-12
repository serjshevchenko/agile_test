import asyncio
import logging
import typing as t
import json

from aiohttp import web
from aioredis import Redis

from app.lib.api import APIClient

log = logging.getLogger()

def clean_cache(app: web.Application) -> None:
    pass


async def store_all_images(app: web.Application) -> None:
    api: APIClient = app['api_client']
    data = await api.images_list(page=1)

    page_count = 0
    if 'pageCount' in data:
        page_count = data['pageCount']

    asyncio.create_task(
        process_pictures(app, data.get('pictures') or [])
    )

    if page_count:
        for page in range(2, page_count):
            log.info(f'process page={page}')
            data = await api.images_list(page=page)
            pictures = data.get('pictures') or []
            if not pictures:
                break
            asyncio.create_task(
                process_pictures(app, pictures)
            )


async def process_pictures(app: web.Application, pictures: t.List[t.Dict[str, t.Any]]) -> None:
    for pic in pictures:
        asyncio.create_task(store_image(app, pic))


async def store_image(app: web.Application, pic: t.Dict[str, t.Any]) -> None:
    log.info(f'sotre picture {pic["id"]}')

    api: APIClient = app['api_client']
    redis: Redis = app['redis']

    pic_data = await api.images_view(pic['id'])

    await redis.set(pic['id'], json.dumps(pic_data))


    log.debug(f'picture fields: {list(pic_data.keys())}')

    await asyncio.gather(*[
        create_index(redis, pic['id'], 'author', pic_data.get('author')),
        create_index(redis, pic['id'], 'camera', pic_data.get('camera')),
        create_index(redis, pic['id'], 'tags', pic_data.get('tags')),
    ])


async def create_index(redis: Redis, image_id: str, field: str, value: t.Optional[str]) -> None:
    if not value:
        return
    await asyncio.gather(*[
        redis.sadd(f'meta_{field}_{piece}', image_id)
        for piece in parse_meta_field(value)
    ])


def parse_meta_field(value: str) -> t.Sequence[str]:
    return [
        piece for piece in value.split(' ')
    ]
