from fastapi import FastAPI
from routers.coin_routers import coin_router

app = FastAPI()
app.title="API BCV, FastApi"
app.version="1.0"
app.include_router(coin_router)
app.root_path="/bcv"