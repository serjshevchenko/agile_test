import asyncio
import typing as t
from functools import cached_property

from aiohttp import ClientError, ClientSession, web

API_KEY = '23567b218376f79d9415'
API_HOST = r'http://interview.agileengine.com'

API_AUTH = fr'{API_HOST}/auth'
API_IMAGE_LIST = fr'{API_HOST}/images'
API_IMAGE_VIEW = fr'{API_HOST}/images/{{id}}'


class APIError(Exception):
    pass


class EmptyAuthToken(APIError):
    pass


class APIClient:
    def __init__(self, app: web.Application) -> None:
        self.app = app

        self.auth_token = None

    @cached_property
    def session(self) -> ClientSession:
        return self.app['session']

    @property
    def auth_headers(self) -> t.Dict[str, str]:
        if not self.auth_token:
            raise EmptyAuthToken()
        return {
            'Authorization': f'Bearer {self.auth_token}',
        }

    async def auth(self) -> None:
        payload = {'apiKey': API_KEY}
        async with self.session.post(API_AUTH, json=payload) as resp:
            resp.raise_for_status()
            self.auth_token = (await resp.json()).get('token')
            assert self.auth_token

    async def images_list(self, page: int = 1, *, retries: int = 3) -> t.List[t.Dict[str, t.Any]]:
        url = API_IMAGE_LIST
        params = {'page': page} if page > 1 else None
        async with self.session.get(url, headers=self.auth_headers, params=params) as resp:
            try:
                resp.raise_for_status()
            except (web.HTTPUnauthorized, EmptyAuthToken):
                await self.auth()
                return await self.images_list(page, retries=retries - 1)
            except (ClientError, asyncio.TimeoutError):
                return await self.images_list(page, retries=retries - 1)

            return await resp.json()

    async def images_view(self, image_id: str, *, retries: int = 3) -> t.List[t.Dict[str, t.Any]]:
        url = API_IMAGE_VIEW.format(id=image_id)
        async with self.session.get(url, headers=self.auth_headers) as resp:
            try:
                resp.raise_for_status()
            except (web.HTTPUnauthorized, EmptyAuthToken):
                await self.auth()
                return await self.images_view(image_id, retries=retries - 1)
            except (ClientError, asyncio.TimeoutError):
                return await self.images_view(image_id, retries=retries - 1)

            return await resp.json()
