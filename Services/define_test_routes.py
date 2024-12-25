from aiohttp import web
from aiohttp.web import AppRunner
import asyncio, aiohttp

tests=[]

async def post_test(req):
    data=await req.json()
    tests.append(data)
    return web.json_response("Added")

async def get_tests(req):
    return web.json_response(tests)

if __name__=="__main__":
    app = web.Application()
    app.router.add_post('/test', post_test)
    app.router.add_get("/test", get_tests)
    web.run_app(app, port=8081)