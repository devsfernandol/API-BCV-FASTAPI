from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from config.config_base import SessionLocal
from models.coin import Price
from routers.coin_routers import coin_router

app = FastAPI()

app.include_router(coin_router)