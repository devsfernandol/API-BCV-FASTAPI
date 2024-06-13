from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from config.config_base import Base


class Price(Base):
    __tablename__ = "prices"
    currency = Column(String, primary_key=True, index=True)
    value = Column(Float, index=True)
