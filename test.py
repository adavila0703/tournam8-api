from fastapi import FastAPI, Request, Response
from src.vars.vars import Env
from pymongo import MongoClient


app = FastAPI()


@app.get('/{test}')
async def home(res: Response, req: Request, test):
    print(type(test))
    return "Welcome to the Tournam8 API!!!"

@app.post('/hi')
async def hi(res: Response, req: Request):
    body = await req.json()
    print(body)