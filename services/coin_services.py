import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from config.config_base import SessionLocal
from models.coin import Price



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
