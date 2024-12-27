import os
import time
from random import randint, choice
import asyncio, aiohttp

from fastapi import FastAPI
from pydantic import BaseModel

tests=[]
class TestParams(BaseModel):
    lat:float 
    cnt:int 
    run:bool
    url:str
    tests:list
    duration:int

app = FastAPI()

async def run_test(test_select, url):
    
        if test_select.get("method")=="get":
            async with aiohttp.ClientSession() as session:
                test_start=time.time()
                res=await session.get(url+test_select.get("endpoint"))
                test_end=time.time()
                return (await res.json(), test_end-test_start)
        elif test_select.get("method")=="post":
            async with aiohttp.ClientSession() as session:
                test_start=time.time()
                res=await session.post(url+test_select.get("endpoint"), json=test_select.get("payload"))
                test_end=time.time()
                return (await res.json(), test_end-test_start)
        elif test_select.get("method")=="put":
            async with aiohttp.ClientSession() as session:
                test_start=time.time()
                res=await session.put(url+test_select.get("endpoint"), json=test_select.get("payload"))
                test_end=time.time()
                return (await res.json(), test_end-test_start)
        elif test_select.get("method")=="patch":
            async with aiohttp.ClientSession() as session:
                test_start=time.time()
                res=await session.patch(url+test_select.get("endpoint"), json=test_select.get("payload"))
                test_end=time.time()
                return (await res.json(), test_end-test_start)
        elif test_select.get("method")=="delete":
            async with aiohttp.ClientSession() as session:
                test_start=time.time()
                res=await session.delete(url+test_select.get("endpoint"))
                test_end=time.time()
                return (await res.json(), test_end-test_start)
        else:
            pass
    
    
        

@app.post("/post_test")
async def test(testParams:TestParams):
        params=testParams.model_dump()

        lat=params.get("lat") 
        cnt=params.get("cnt") 
        run=params.get("run")
        url=params.get("url")
        tests=params.get("tests")
        duration=params.get("duration")

        lock = asyncio.Lock()
        start=time.time()
        while run:
            running= time.time()
            if running - start >= duration:
                run = False
            else:
                test_select = choice(tests)
                
                res_stat= await run_test(test_select, url)
                if res_stat[0]:
                    async with lock:
                        cnt += 1
                        latency=res_stat[1]
                        if(lat<latency):
                            lat = latency
        return {"cnt": cnt, "lat":lat}

