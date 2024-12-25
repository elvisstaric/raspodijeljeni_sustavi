from aiohttp import web
from aiohttp.web import AppRunner
import asyncio, aiohttp

test_settings={}

async def post_params(req):
    data=await req.json()
    new_url=data.get("url")
    try:
        async with aiohttp.ClientSession() as session: 
            await session.get(new_url)
            test="Stranica postoji" 
            test_settings.update(data)
    except:
        test="Stranica ne postoji!"
        test_settings.clear()
    return web.json_response(test)

async def get_handler(req):
    return web.json_response(test_settings)

if __name__=="__main__":
    app = web.Application()
    app.router.add_post('/post_params', post_params)
    app.router.add_get("/values", get_handler)
    web.run_app(app)