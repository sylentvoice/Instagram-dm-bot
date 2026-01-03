from instagrapi import Client
import time
import random
import os

cl = Client()

SESSIONID = os.getenv("IG_SESSIONID")
cl.login_by_sessionid(SESSIONID)

me_id = cl.user_id
my_username = cl.username
print(f"🤖 Logged in as @{my_username} (ID: {me_id})")

reply_templates_master = [
"""ARJUN TRY M4AA R4xNDY🤎_____________/




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

def get_next_reply(username, history):
    possible_replies = [r for r in reply_templates_master if r not in history]
    if not possible_replies:
        history.clear()
        possible_replies = reply_templates_master.copy()

    reply = random.choice(possible_replies)
    history.add(reply)
    return reply.replace("{user}", username)

def auto_reply():
    while True:
        try:
            threads = cl.direct_threads(amount=5)

            for thread in threads:
                if not thread.messages:
                    continue

                latest_msg = thread.messages[0]

                if latest_msg.user_id == me_id:
                    continue

                user_id = latest_msg.user_id
                username = thread.users[0].username

                if last_msg_id_by_user.get(user_id) == latest_msg.id:
                    continue

                if user_id not in user_reply_history:
                    user_reply_history[user_id] = set()

                reply = get_next_reply(username, user_reply_history[user_id])

                try:
                    cl.direct_answer(thread.id, reply)
                    print(f"✔️ Replied to @{username}")
                    last_msg_id_by_user[user_id] = latest_msg.id
                    time.sleep(15)
                except Exception as e:
                    print(f"⚠️ Reply failed: {e}")

            time.sleep(15)

        except Exception as err:
            print(f"🚨 Main loop error: {err}")
            time.sleep(15)

auto_reply()
