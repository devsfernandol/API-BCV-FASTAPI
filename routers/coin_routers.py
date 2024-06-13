from fastapi import APIRouter
from fastapi import  HTTPException
from config.config_base import SessionLocal
from models.coin import Price
from config.config_base import Base, engine
from services.coin_services import update_prices


coin_router= APIRouter()




@coin_router.on_event("startup")
async def startup_event():
   Base.metadata.create_all(bind=engine)  # Crear base de datos 
   update_prices() #actulizar coin 

@coin_router.get("/prices")
def read_prices():
    db = SessionLocal()
    prices = db.query(Price).all()
    db.close()
    return {price.currency: price.value for price in prices}

@coin_router.post("/update-prices")
def force_update_prices():
    try:
        update_prices()
        return {"message": "Prices updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))