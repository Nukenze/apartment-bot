import requests
import time
import threading
from flask import Flask

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
    print("BOT STARTED")

    seen = set()

    while True:
        try:
            print("Checking site...")

            res = requests.get(URL, timeout=15)
            html = res.text.lower()

            if "1 bed" in html or "1 bedroom" in html:
                if "1bed" not in seen:
                    send_message("🔥 Появилась 1 bedroom квартира!\n" + URL)
                    seen.add("1bed")
                    print("FOUND 1 BEDROOM")

            else:
                print("No 1 bedroom yet")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(CHECK_INTERVAL)

# ===== ФОН =====
def start_bot():
    check_site()

# ===== KEEP ALIVE =====
@app.route("/")
def home():
    return "Bot is running"

# ===== ЗАПУСК =====
if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
