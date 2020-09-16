import asyncio
import concurrent

from aiohttp import web

from json_store import JsonStore

_pool = concurrent.futures.ProcessPoolExecutor()


async def get(request):
    return web.json_response(js.get())


async def get_post_id(request):
    id_ = request.match_info.get('id', -1)
    if id_.isdigit():
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(_pool, js.get_by_id, int(id_))
        if r is not None:
            return web.json_response(r)
    return web.HTTPNotFound()



if __name__ == '__main__':
    js = JsonStore()
    app = web.Application()
    app.add_routes([web.get('/', get),
                    web.get('/post/{id}', get_post_id)])
    web.run_app(app)
