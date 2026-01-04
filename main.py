from instagrapi import Client
import time
import random
import os
import threading
from flask import Flask

# =================================================
# 🔹 Flask server (ONLY to bind port for Render)
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


# Start Flask in background
threading.Thread(target=run_flask, daemon=True).start()

# =================================================
# 🔹 Instagram Client Setup
# =================================================
cl = Client()

SESSIONID = os.getenv("IG_SESSIONID")
if not SESSIONID:
    raise Exception("❌ IG_SESSIONID not set in environment variables")

cl.login_by_sessionid(SESSIONID)

me_id = cl.user_id
my_username = cl.username
print(f"🤖 Logged in as @{my_username} (ID: {me_id})")

# =================================================
# 🔹 Reply Templates
# =================================================
reply_templates_master = [
"""ARJUN TRY M4AA R4xNDY🤎_______________/




ARJUN TRY M4AA R4xNDY💛_______________/




ARJUN TRY M4AA R4xNDY💚_______________/




ARJUN TRY M4AA R4xNDY❤️‍🩹_______________/




ARJUN TRY M4AA R4xNDY❤️_______________/




ARJUN TRY M4AA R4xNDY💙_______________/




ARJUN TRY M4AA R4xNDY💜_______________/"""
]

#🧠 Maintain last message replied for each user
last_msg_id_by_user = {}

def get_next_reply(username, history):
    # Filter replies jo already iss user ko bheje gaye ho
    possible_replies = [r for r in reply_templates_master if r not in history]
    if not possible_replies:
        history.clear()
        possible_replies = reply_templates_master.copy()
    reply = random.choice(possible_replies)
    history.add(reply)
    return reply.replace("{user}", username)

user_reply_history = {}

def auto_reply():
    while True:
        try:
            threads = cl.direct_threads(amount=1)

            for thread in threads:
                if not thread.messages:
                    continue

                latest_msg = thread.messages[0]

                # Apna msg ignore karo
                if latest_msg.user_id == me_id:
                    continue

                user_id = latest_msg.user_id
                username = cl.user_info(user_id).username

                # Agar same msg pe already reply kar chuke ho, skip karo
                if last_msg_id_by_user.get(user_id) == latest_msg.id:
                    continue

                # User history init if not exists
                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                # 📨 Generate new random reply
                reply = get_next_reply(username, user_reply_history[user_id])

                try:
                    cl.direct_answer(thread.id, reply)
                    print(f"✔️ Replied to @{username}: {reply}")
                    last_msg_id_by_user[user_id] = latest_msg.id
                    time.sleep(random.randint(11, 22))
                except Exception as e:
                    print(f"⚠️ Failed to reply in thread {thread.id}: {e}")

            time.sleep(random.randint(12, 23))

        except Exception as err:
            print(f"🚨 Main loop error: {err}")
            time.sleep(random.randint(10, 20))

# 🚀 Start bot
auto_reply()
