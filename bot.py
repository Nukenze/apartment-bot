from flask import Flask
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests

# ----------- WEB SERVER -----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)


# ----------- BOT -----------
URL = "https://jadeevt.com/floorplans/"

TOKEN = "8773988746:AAHyYE2b18iC_DN0WuCaurl52V0BGjpayBc"
CHAT_ID = "494628479"

seen = set()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def run_bot():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    while True:
        try:
            driver.get(URL)
            time.sleep(5)

            cards = driver.find_elements(By.XPATH, "//div[contains(@class,'floorplan')]")

            current = set()

            for card in cards:
                text = card.text.lower()

                if "1 bed" in text or "1 bedroom" in text:
                    if "available" in text:
                        info = card.text.strip()
                        current.add(info)

                        if info not in seen:
                            send_telegram(f"🔥 Новая 1BR квартира:\n\n{info}")

            seen.clear()
            seen.update(current)

            print("checking 1BR...")

        except Exception as e:
            print("error:", e)

        time.sleep(60)


# ----------- RUN BOTH -----------
threading.Thread(target=run_web).start()
threading.Thread(target=run_bot).start()
