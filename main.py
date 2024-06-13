from fastapi import FastAPI
from routers.coin_routers import coin_router

app = FastAPI()

app.include_router(coin_router)