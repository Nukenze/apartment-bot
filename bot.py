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

def check_site():
    print("BOT STARTED")

    seen = False

    while True:
        try:
            print("Checking site...")

            res = requests.get(URL, timeout=15)
            html = res.text.lower()

            if "1 bed" in html or "1 bedroom" in html:
                if not seen:
                    send_message("🔥 Есть 1 bedroom!\n" + URL)
                    seen = True
                    print("FOUND")

            else:
                print("Nothing yet")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(600)

@app.route("/")
def home():
    return "Bot is running"

def run_bot():
    check_site()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
