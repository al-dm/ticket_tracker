import requests
import json
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = os.environ["URL"]
LIMIT = 9000



def get_low_price(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)

            if "offers" in data and "lowPrice" in data["offers"]:
                return float(data["offers"]["lowPrice"])

        except (json.JSONDecodeError, TypeError):
            continue

    return None


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )


price = get_low_price(URL)

print("Текущая цена:", price)

if price is not None and price < LIMIT:
    send_telegram(
        f"🎫 Цена упала!\n"
        f"Сейчас: {price:.0f} ₽\n"
        f"{URL}"
    )


if price is not None and price > LIMIT:
    send_telegram(
        f"🎫 Цена выросла!\n"
        f"Сейчас: {price:.0f} ₽\n"
        f"{URL}"
    )
