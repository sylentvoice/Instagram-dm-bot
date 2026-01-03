from instagrapi import Client
import time
import random
import os
import threading
from flask import Flask

# -------------------------------
# 🔹 Flask server (ONLY for Render port binding)
# -------------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# -------------------------------
# 🔹 Instagram Client
# -------------------------------
cl = Client()

SESSIONID = os.getenv("IG_SESSIONID")
if not SESSIONID:
    raise Exception("❌ IG_SESSIONID not set in environment variables")

cl.login_by_sessionid(SESSIONID)

me_id = cl.user_id
my_username = cl.username
print(f"🤖 Logged in as @{my_username} (ID: {me_id})")

# -------------------------------
# 🔹 Reply templates
# -------------------------------
reply_templates_master = [
"""ARJUN TRY M4AA R4xNDY🤎_______________/




ARJUN TRY M4AA R4xNDY💛_______________/




ARJUN TRY M4AA R4xNDY💚_______________/




ARJUN TRY M4AA R4xNDY❤️‍🩹_______________/




ARJUN TRY M4AA R4xNDY❤️_______________/




ARJUN TRY M4AA R4xNDY💙_______________/




ARJUN TRY M4AA R4xNDY💜_______________/""",
    """ARJUN TMKC FAD DUGA BIHARI BAXHE/////////////////~~~~🎀


__________________________________________________________________



ARJUN TMKB MEIN A44G LGA DUGA///////////////////~~~~❤️‍🩹



ARJUN TMKB BOXDA NHI JAW4LA MUKHI HAI/////////////////~~~~🎀


__________________________________________________________________




ARJUN BETA P4P4 KE LWWWD333 KO FEEL KR//////////////////~~~~💜❤️💛💙🩷💚



ARJUN TMKC FAD DUGA BIHARI BAXHE/////////////////~~~~🎀


__________________________________________________________________



💚🩷💙💛❤️💜💜❤️‍🩹🎀👽🦢☃️




ARJUN TMKC FAD DUGA BIHARI BAXHE/////////////////~~~~🎀


__________________________________________________________________


ARJUN FUXXXXK3D///////~~❤️‍🩹🙄🫴"""
]

last_msg_id_by_user = {}
user_reply_history = {}

# -------------------------------
# 🔹 Helper function
# -------------------------------
def get_next_reply(username, history):
    possible = [r for r in reply_templates_master if r not in history]
    if not possible:
        history.clear()
        possible = reply_templates_master.copy()

    reply = random.choice(possible)
    history.add(reply)
    return reply.replace("{user}", username)

# -------------------------------
# 🔹 Main bot loop
# -------------------------------
def auto_reply():
    while True:
        try:
            print("⏳ Bot alive, checking inbox...")

            threads = cl.direct_threads(amount=5)

            for thread in threads:
                if not thread.messages:
                    continue

                latest_msg = thread.messages[0]

                # Ignore own messages
                if latest_msg.user_id == me_id:
                    continue

                user_id = latest_msg.user_id
                username = thread.users[0].username

                # Prevent duplicate replies
                if last_msg_id_by_user.get(user_id) == latest_msg.id:
                    continue

                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                reply = get_next_reply(username, user_reply_history[user_id])

                cl.direct_answer(thread.id, reply)
                print(f"✅ Replied to @{username}")

                last_msg_id_by_user[user_id] = latest_msg.id

                # Human-like delay
                time.sleep(random.randint(10, 20))

            time.sleep(random.randint(10, 20))

        except Exception as e:
            print(f"🚨 Error: {e}")
            time.sleep(30)

# -------------------------------
# 🚀 Start bot
# -------------------------------
auto_reply()
