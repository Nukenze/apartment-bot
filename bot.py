import requests
import time
import threading
from flask import Flask
from bs4 import BeautifulSoup

# ===== НАСТРОЙКИ =====
TOKEN = "8773988746:AAHyYE2b18iC_DN0WuCaurl52V0BGjpayBc"
CHAT_ID = "494628479"
URL = "https://jadeevt.com/floorplans/"

CHECK_INTERVAL = 600  # 10 минут

app = Flask(__name__)

# ===== TELEGRAM =====
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# ===== ПАРСИНГ =====
def check_site():
    print("🔥 BOT STARTED")

    seen = False

    while True:
        try:
            print("Checking site...")

            res = requests.get(URL, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")

            found = False

            # ищем любые блоки с текстом
            for unit in soup.find_all("div"):
                text = unit.get_text().lower()

                if "1 bed" in text or "1 bedroom" in text:
                    found = True
                    break

            if found:
                print("FOUND 1 BEDROOM")

                if not seen:
                    send_message("🔥 Появилась 1 bedroom квартира!\n" + URL)
                    seen = True
            else:
                print("Nothing yet")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(CHECK_INTERVAL)

# ===== KEEP ALIVE =====
@app.route("/")
def home():
    return "Bot is running"

# ===== ЗАПУСК =====
if __name__ == "__main__":
    threading.Thread(target=check_site).start()
    app.run(host="0.0.0.0", port=10000)
