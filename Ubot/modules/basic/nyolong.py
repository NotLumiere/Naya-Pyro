# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
# kenkan
# abdul
# recode dikit #amang
# All rights reserved.

import os

from pyrogram import *
from pyrogram.errors import RPCError
from pyrogram.types import *
from ubotlibs.ubot.utils import get_arg

from Ubot.core.db import get_botlog

from . import *


@Ubot("copy", "")
async def nyolongnih(client, message):
    await message.edit("Processing...")
    link = get_arg(message)
    msg_id = int(link.split("/")[-1])
    if "t.me/c/" in link:
        try:
            chat = int("-100" + str(link.split("/")[-2]))
            dia = await client.get_messages(chat, msg_id)
        except RPCError:
            await message.edit("Sepertinya terjadi kesalahan")
    else:
        try:
            chat = str(link.split("/")[-2])
            dia = await client.get_messages(chat, msg_id)
        except RPCError:
            await message.edit("Sepertinya terjadi kesalahan")
    anjing = dia.caption or None
    if dia.text:
        await dia.copy(message.chat.id)
        await message.delete()
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.video:
        anu = await client.download_media(dia)
        await client.send_video(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.audio:
        anu = await client.download_media(dia)
        await client.send_audio(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.voice:
        anu = await client.download_media(dia)
        await client.send_voice(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.document:
        anu = await client.download_media(dia)
        await client.send_document(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
    else:
        await message.edit("Sepertinya terjadi kesalahan")


@Ubot("curi", "")
async def pencuri(client, message):
    dia = message.reply_to_message
    user_id = client.me.id
    botlog_chat_id = await get_botlog(user_id)
    if not dia:
        await message.edit("Mohon balas ke media")
    anjing = dia.caption or None
    await message.edit("Processing...")
    if dia.text:
        await dia.copy(botlog_chat_id)
        await message.delete()
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo(botlog_chat_id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.video:
        anu = await client.download_media(dia)
        await client.send_video(botlog_chat_id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.audio:
        anu = await client.download_media(dia)
        await client.send_audio(botlog_chat_id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.voice:
        anu = await client.download_media(dia)
        await client.send_voice(botlog_chat_id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.document:
        anu = await client.download_media(dia)
        await client.send_document(botlog_chat_id, anu, anjing)
        await message.delete()
        os.remove(anu)
    else:
        await message.edit("Sepertinya terjadi kesalahan")


add_command_help(
    "nyolong",
    [
        ["copy <link protected channel.>", "Clone restricted media."],
        ["curi <reply message>", "Clone from the protected media or timer message."],
    ],
)
