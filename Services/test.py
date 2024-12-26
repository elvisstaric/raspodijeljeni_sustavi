import os
import time
from random import randint, choice
import asyncio, aiohttp

from multiprocessing import Process, Value, Lock, Manager

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
    
    
        


def test(lat, cnt, run, url, tests):
        max_lat=0
        now = time.time()
        
        while run.value:
            test_select = choice(tests)
            
            res_stat= asyncio.run(run_test(test_select, url))
            if res_stat[0]:
                with cnt.get_lock():
                    cnt.value += 1
                latency=res_stat[1]
                with lat.get_lock():
                    if(lat.value<latency):
                        lat.value = latency


def test_controler(lat,cnt, run, start, gl_start, duration, interval, results):
        while run.value:
            now = time.time()
            if now - gl_start >= duration:
                run.value = False
            if now - start.value >= interval:
                print("Responses:", cnt.value, "lat:", lat.value,)
                results.append({"time": now-gl_start, "Responses:": cnt.value, "lat:": lat.value,})
                with cnt.get_lock():
                    cnt.value = 0
                with lat.get_lock():
                    lat.value=0
                with start.get_lock():
                    start.value = now

async def main():
    params = await get_params()
    url=params.get("url")
    clients=params.get("clients")
    duration=params.get("test_duration")+1
    interval=params.get("interval")

    tests = await get_routes()

    if __name__ == '__main__':
        cnt = Value('i', 0)
        start = Value('d', 0.0)
        lat = Value("d", 0.0)
        processes = []
        start.value = gl_start = time.time()
        run = Value('b', True)
        results = Manager().list()

        for i in range(clients):
            process = Process(target=test, args=(lat,cnt, run, url, tests))
            process.start()
            processes.append(process)
        process = Process(target=test_controler, args=(lat,cnt, run, start, gl_start, duration, interval, results))
        process.start()
        processes.append(process)

        for process in processes:
            process.join()
        print(results)
        
        
asyncio.run(main())