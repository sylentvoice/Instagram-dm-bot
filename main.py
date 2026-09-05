from instagrapi import Client
import time
import random
import os
from keep_alive import keep_alive

keep_alive()

cl = Client()

# 🔐 Session ID Render Environment Variable se li jayegi
session_id = os.getenv("INSTAGRAM_SESSION_ID")

if not session_id:
    raise RuntimeError("INSTAGRAM_SESSION_ID environment variable is not set")

cl.login_by_sessionid(session_id)

me_id = cl.user_id
my_username = cl.username
print(f"🤖 Logged in as @{my_username} (ID: {me_id})")

# ✅ Message reply templates (edit if you want)
reply_templates_master = [
    """𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼🩵___________________//////////











𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼👽___________________//////////












𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼💅___________________//////////












𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼🍧___________________//////////












𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼🌸___________________//////////













𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼🧁___________________//////////














𝑺𝑯𝑬𝑵𝑼//𝑹𝑨𝑯𝑼𝑳 𝑻𝑬𝑹𝒀 𝑴𝑨𝑨 𝑹𝑵𝑫 𝑩𝑵𝑨𝑲𝑬 𝑩𝑯𝑨𝑮𝑼🎀___________________//////////
""",
    """𝑺𝑯𝑬𝑵𝑼 𝒀𝑨𝑾𝑳 𝑨𝑨𝑷 𝑻𝑶 𝑩𝑨𝑻𝑯𝑹𝑶𝑶𝑴 𝑺𝑻𝑨𝑹 𝑯𝑶𝑾//////-------------👅










𝑺𝑯𝑬𝑵𝑼 𝒀𝑨𝑾𝑳 𝑨𝑨𝑷 𝑻𝑶 𝑩𝑨𝑻𝑯𝑹𝑶𝑶𝑴 𝑺𝑻𝑨𝑹 𝑯𝑶𝑾 //////-------------👅










 
 𝑺𝑯𝑬𝑵𝑼 𝑻𝑴𝑹 𝑪𝒀𝑼 𝑯𝑨𝑰 𝒀𝑨𝑾𝑳//////-------------👅










𝑺𝑯𝑬𝑵𝑼 𝑻𝑴𝑹 𝑪𝒀𝑼 𝑯𝑨𝑰 𝒀𝑨𝑾𝑳 //////-------------👅









𝑺𝑯𝑬𝑵𝑼 𝑻𝑴𝑹 𝑪𝒀𝑼 𝑯𝑨𝑰 𝒀𝑨𝑾𝑳 //////-------------👅








𝑺𝑯𝑬𝑵𝑼 𝑻𝑴𝑹 𝑪𝒀𝑼 𝑯𝑨𝑰 𝒀𝑨𝑾𝑳 //////-------------👅
"""
    
]

# 🧠 Maintain last message replied for each user
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
                reply = get_next_reply(
                    username,
                    user_reply_history[user_id]
                )

                try:
                    cl.direct_answer(thread.id, reply)
                    print(f"✔️ Replied to @{username}: {reply}")
                    last_msg_id_by_user[user_id] = latest_msg.id
                    time.sleep(random.randint(22, 51))
                except Exception as e:
                    print(f"⚠️ Failed to reply in thread {thread.id}: {e}")

            time.sleep(random.randint(16, 34))

        except Exception as err:
            print(f"🚨 Main loop error: {err}")
            time.sleep(random.randint(10, 29))

# 🚀 Start bot
auto_reply()