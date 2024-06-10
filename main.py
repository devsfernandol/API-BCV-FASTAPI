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

app = FastAPI()

def get_prices(url):
    html_text = requests.get(url, verify=False).text
    soup = BeautifulSoup(html_text, 'html.parser')
    prince_with_eur = soup.find_all("strong")
    prices = {}
    titles = ["titulo1", "titulo2", "EUR", "CNY", "TRY", "RUB", "USD"]
    for i, element in enumerate(prince_with_eur):
        if i < len(titles) and titles[i] not in ["titulo1", "titulo2"]:
            price_text = element.text.strip().replace(',', '.')
            prices[titles[i]] = float(price_text)
    return prices

def update_prices():
    url = "https://www.bcv.org.ve"
    prices = get_prices(url)
    db = SessionLocal()
    try:
        for currency, value in prices.items():
            price_record = db.query(Price).filter(Price.currency == currency).first()
            if price_record:
                price_record.value = value
            else:
                db.add(Price(currency=currency, value=value))
        db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(update_prices, 'interval', hours=1)
scheduler.start()

@app.on_event("startup")
async def startup_event():
    update_prices()  # Actualizar los precios al iniciar la aplicación

@app.get("/prices")
def read_prices():
    db = SessionLocal()
    prices = db.query(Price).all()
    db.close()
    return {price.currency: price.value for price in prices}

@app.post("/update-prices")
def force_update_prices():
    try:
        update_prices()
        return {"message": "Prices updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

