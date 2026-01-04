from instagrapi import Client
import time
import random
import os
import threading
from flask import Flask

# =================================================
# 🔹 Flask server (ONLY for port binding)
# =================================================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

@app.route("/favicon.ico")
def favicon():
    return "", 204

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Start Flask in background thread
threading.Thread(target=run_flask, daemon=True).start()

# =================================================
# 🔹 Instagram Client
# =================================================
cl = Client()
cl.login_by_sessionid(os.getenv("IG_SESSIONID"))

me_id = cl.user_id
print(f"🤖 Logged in as @{cl.username}")

# =================================================
# 🔹 Reply templates
# =================================================
reply_templates_master = ["""ARJUN TRY M4AA R4xNDY🤎_______________/




ARJUN TRY M4AA R4xNDY💛_______________/




ARJUN TRY M4AA R4xNDY💚_______________/




ARJUN TRY M4AA R4xNDY❤️‍🩹_______________/




ARJUN TRY M4AA R4xNDY❤️_______________/




ARJUN TRY M4AA R4xNDY💙_______________/




ARJUN TRY M4AA R4xNDY💜_______________/"""]

last_msg_id_by_user = {}
user_reply_history = {}

def get_next_reply(history):
    possible = [r for r in reply_templates_master if r not in history]
    if not possible:
        history.clear()
        possible = reply_templates_master.copy()
    reply = random.choice(possible)
    history.add(reply)
    return reply

# =================================================
# 🔹 Bot loop
# =================================================
def auto_reply():
    while True:
        try:
            threads = cl.direct_threads(amount=1)

            for thread in threads:
                if not thread.messages:
                    continue

                msg = thread.messages[0]
                if msg.user_id == me_id:
                    continue

                user_id = msg.user_id
                username = thread.users[0].username

                if last_msg_id_by_user.get(user_id) == msg.id:
                    continue

                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                reply = get_next_reply(user_reply_history[user_id])
                cl.direct_answer(thread.id, reply)

                print(f"✔️ Replied to @{username}")
                last_msg_id_by_user[user_id] = msg.id

                time.sleep(random.randint(10, 20))

            time.sleep(random.randint(10, 20))

        except Exception as e:
            print("🚨 Error:", e)
            time.sleep(30)

# =================================================
# 🚀 Start bot
# =================================================
auto_reply()
