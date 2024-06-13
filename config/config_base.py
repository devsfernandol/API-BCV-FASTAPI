from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

class Price(Base):
    __tablename__ = "prices"
    currency = Column(String, primary_key=True, index=True)
    value = Column(Float, index=True)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)