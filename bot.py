import requests
import time
import threading
from flask import Flask

TOKEN = "8773988746:AAHyYE2b18iC_DN0WuCaurl52V0BGjpayBc"
CHAT_ID = "494628479"
URL = "https://jadeevt.com/floorplans/"

app = Flask(__name__)

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

@app.route("/")
def home():
    return "Bot is alive"

# ===== ГЛАВНАЯ ЛОГИКА =====
def run_bot():
    print("🔥 BOT STARTED")

    seen = False

    while True:
        try:
            print("Checking site...")

            res = requests.get(URL, timeout=15)
            html = res.text.lower()

            if "1 bed" in html or "1 bedroom" in html:
                if not seen:
                    send_message("🔥 1 bedroom найден!\n" + URL)
                    seen = True
                    print("FOUND 1 BEDROOM")

            else:
                print("Nothing yet")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(60)  # пока 1 минута для теста

# ===== ЗАПУСК =====
if __name__ == "__main__":
    # Flask отдельно
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()

    # Бот напрямую (НЕ в фоне)
    run_bot()
