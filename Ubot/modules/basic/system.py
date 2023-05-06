import asyncio
import math
import sys
from os import remove

import heroku3
import requests
import urllib3
from pyrogram import *
from pyrogram.types import *
from ubotlibs.ubot.utils.misc import *

from config import *
from Ubot import *
from Ubot.core.db import *
from Ubot.logging import LOGGER
from Ubot.modules.basic import *

from . import *

HAPP = None


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


@Client.on_message(filters.command("restart", "") & filters.me)
async def restart_bot(client, message):
    try:
        await message.reply("Restarting bot...")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return

    await message.reply("✅ Bot has restarted.")
    client.restart()


@Ubot("usage", "")
async def usage_dynos(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>Menggunakan App Heroku!</b>\n\nMasukan/atur  `HEROKU_API_KEY` dan `HEROKU_APP_NAME` untuk bisa melakukan update!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>Menggunakan App Heroku!</b>\n\n<b>pastikan</b> `HEROKU_API_KEY` **dan** `HEROKU_APP_NAME` <b>sudah di configurasi dengan benar!</b>"
            )
    else:
        return await message.reply_text("Hanya untuk Heroku Deployment")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " Pastikan Heroku API Key, App name sudah benar"
        )
    dyno = await message.reply_text("Memeriksa penggunaan dyno...")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
**Penggunaan Dyno Naya-Premium**

 ❏ Dyno terpakai:
 ├ Terpakai: `{AppHours}`**h**  `{AppMinutes}`**m**  [`{AppPercentage}`**%**]
Dyno tersisa:
  ╰ Tersisa: `{hours}`**h**  `{minutes}`**m**  [`{percentage}`**%**]"""
    return await dyno.edit(text)


@Ubot("shutdown", "")
async def shutdown_bot(client, message):
    botlog_chat_id = await get_log_groups(user_id)
    if not botlog_chat_id:
        return await message.reply(
            "`Maaf, tidak dapat menemukan ID chat log bot.`\nPastikan Anda Telah Mengtur Log Group Anda"
        )
    await client.send_message(
        botlog_chat_id,
        "**#SHUTDOWN** \n"
        "**Naya-Premium** telah di matikan!\nJika ingin menghidupkan kembali silahkan buka heroku",
    )
    await message.reply(" **Naya-Premium Berhasil di matikan!**")
    if HAPP is not None:
        HAPP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@Ubot("logs", "")
async def logs_ubot(client, message):
    if HAPP is None:
        return await message.reply(
            "Pastikan `HEROKU_API_KEY` dan `HEROKU_APP_NAME` anda dikonfigurasi dengan benar di config vars heroku",
        )
    biji = await message.reply("🧾 `Get Logs your Bots...`")
    with open("Logs-Heroku.txt", "w") as log:
        log.write(HAPP.get_log())
    await client.send_document(
        message.chat.id,
        "Logs-Heroku.txt",
        thumb="https://telegra.ph//file/976ad753d6073dde1f579.jpg",
        caption="**This is your Heroku Logs**",
    )
    await biji.delete()
    remove("Logs-Heroku.txt")
