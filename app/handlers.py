import json

from aiohttp import web

from app.bl.images import search_pictures


async def search_by_term(request: web.Request) -> web.Response:
    app = request.app
    term = request.match_info['term']
    data = await search_pictures(app, term)
    return web.HTTPOk(
        content_type='application/json',
        body=json.dumps({'data': data})
    )

