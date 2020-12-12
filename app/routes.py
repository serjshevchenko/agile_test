from aiohttp import web

from app.handlers import search_by_term


def setup_routes(app: web.Application) -> None:
    app.router.add_get('/search/{terms}', search_by_term)
