from typing import Literal, Optional

from fastapi import FastAPI
from pydantic import BaseModel

tests=[]
class Test(BaseModel):
    method:Literal["get", "post", "put", "patch", "delete"]
    endpoint: str 
    payload: Optional[dict]=None



app=FastAPI()

@app.post("/test")
async def post_test(test:Test):
    data=test.model_dump()
    tests.append(data)
    return ("Added")

@app.get("/test")
async def get_tests():
    return {"tests":tests}

