from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream

from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle

import asyncio, json, pytgcalls, random

from config import *

if SESSION_STRING:
    app = Client(
        "call",
        API_ID,
        API_HASH,
        session_string=SESSION_STRING
    )
else:
    app = Client(
        "call",
        API_ID,
        API_HASH
    )
call = PyTgCalls(app)


with open("./quran.json", "r", encoding="utf-8") as f:
    quran = json.loads(f.read())["s"]

already = []

async def Call():
    while not await asyncio.sleep(1.5):
        print(len(already))
        if len(already) == 114:
            already.clear()
        if already:
            surah = quran[already.index(already[-1]) + 1]
        else:
            surah = quran[0]
        if SPECIFIC_READER:
            for i in surah["sounds"]:
                if i["name"] == SPECIFIC_READER:
                    surah_sound = i
                    break
        else:
            surah_sound = random.choice(surah["sounds"])
        sound_name = surah_sound["name"]
        sound_url = surah_sound["url"]
        surah_name = surah["surah"]
        title = f"{surah_name} | {sound_name}"
        try:
            getGroupCall = await call.get_active_call(CHAT_ID)
            if not getGroupCall.is_playing:
                await call.leave_group_call(CHAT_ID)
        except Exception:
            try:
                await call.leave_group_call(CHAT_ID)
            except:
                pass
        try:
            if not CHANNEL_USERNAMWE:
                await call.join_group_call(
                    CHAT_ID,
                    MediaStream(sound_url),
                )
            else:
                await call.join_group_call(
                    CHAT_ID,
                    MediaStream(sound_url),
                    join_as=await app.resolve_peer(CHANNEL_USERNAMWE)
                )
                channel = await app.invoke(GetFullChannel(channel=await app.resolve_peer(CHAT_ID)))
                data = EditGroupCallTitle(call=channel.full_chat.call, title=title)
                await app.invoke(data)
                already.append(surah)
        except pytgcalls.exceptions.AlreadyJoinedError:
                print("Already Joined")
        except Exception as e:
                print(e)

async def main():
    await app.start()
    print("APP START")
    await call.start()
    print("CALL START")
    asyncio.create_task(Call())
    print("DONE")
    await idle()

asyncio.run(main())