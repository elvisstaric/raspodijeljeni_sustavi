import aiohttp

from fastapi import FastAPI
from pydantic import BaseModel, ValidationError

class Settings(BaseModel):
    url:str 
    clients: int 
    test_duration:int 
    interval:int 

app=FastAPI()

test_settings={}

@app.post('/post_params')
async def post_params(settings: Settings):
    data= settings.model_dump()
    new_url=data.get("url")
    try:
        async with aiohttp.ClientSession() as session: 
            await session.get(new_url)
            test="Stranica postoji" 
            test_settings.update(data)
    except:
        test="Stranica ne postoji!"
        test_settings.clear()
    return {test}

@app.get("/values")
async def get_handler():
    return {"settings":test_settings}

