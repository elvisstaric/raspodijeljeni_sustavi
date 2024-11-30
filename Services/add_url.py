from aiohttp import web
from aiohttp.web import AppRunner
import asyncio, aiohttp

url=[]

async def post_url(req):
    new_url=await req.json()
    try:
        async with aiohttp.ClientSession() as session: 
            await session.get(new_url)
            test="Stranica postoji" 
    except:
        test="Stranica se ne postoji!"
    url.append(new_url)
    return web.json_response(test)

app = web.Application()
app.router.add_post('/post_url', post_url)

async def start_server():
    runner = AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("Poslužitelj sluša na http://localhost:8080")

async def main():
    await start_server() 
    async with aiohttp.ClientSession() as session: 

        url=input("Unesite adresu stranice koju zelite testirati: ")
        url_rez=await session.post("http://localhost:8080/post_url", json=url)
        print(await url_rez.text())
asyncio.run(main()) 