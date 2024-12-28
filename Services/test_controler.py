import time
import asyncio, aiohttp
from fastapi import FastAPI


app = FastAPI() 

async def get_params():
    async with aiohttp.ClientSession() as session:
        get_settings=await session.get("http://localhost:8081/values")
        settings = await get_settings.json()
    return settings.get("settings")


async def get_routes():
    async with aiohttp.ClientSession() as session:
        get_settings=await session.get("http://localhost:8082/test")
        tests=await get_settings.json()
    return tests.get("tests")


async def test_controler(lat,cnt, run, start, gl_start, duration, interval, clients, url, tests):
        cnt_all=0
        max_lat=0
        results_all=[]
        while run:
            now = time.time()
            if now - gl_start >= duration:
                run = False
            if now - start >= interval:
                processes=[]
                for i in range(clients):
                    process = test(lat,cnt, run, url, tests, interval)
                    processes.append(process)
                results = await asyncio.gather(*processes)
                for result in results:
                    cnt_all+=result.get("cnt")
                    if max_lat<result.get("lat"):
                        max_lat=result.get("lat")
                print("Responses:", cnt_all, "lat:", max_lat,)
                results_all.append({"time": int(now-gl_start), "Responses:": cnt_all, "lat:": max_lat,})
                cnt_all = 0
                max_lat=0
                start = now
        return results_all
    
async def test(lat,cnt, run, url, tests, duration):
    async with aiohttp.ClientSession() as session:
        params={"lat":lat, "cnt":cnt, "run":run, "url":url, "tests":tests, "duration":duration}
        res=await session.post("http://localhost:8083/post_test", json=params)
        return await res.json()

@app.get("/start_test")
async def testRun():
    params = await get_params()
    url=params.get("url")
    clients=params.get("clients")
    duration=params.get("test_duration")
    duration+=1
    interval=params.get("interval")

    tests = await get_routes()

    
    cnt = 0
    start = 0
    lat = 0
    start = gl_start = time.time()
    run = True

    res= await test_controler(lat,cnt, run, start, gl_start, duration, interval, clients, url, tests)
    return {"results":res}
        
