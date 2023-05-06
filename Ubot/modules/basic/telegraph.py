# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


import os

from pyrogram import Client
from pyrogram.types import Message
from telegraph import Telegraph, exceptions, upload_file
from ubotlibs.ubot.utils.tools import *

from . import *

telegraph = Telegraph()
r = telegraph.create_account(short_name="Naya-Pyro")
auth_url = r["auth_url"]


@Ubot(["tg", "tm"], "")
async def uptotelegraph(client: Client, message: Message):
    tex = await message.edit_text("`Processing . . .`")
    if not message.reply_to_message:
        await tex.edit("**Balas ke File atau Teks**")
        return
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            m_d = await convert_to_image(message, client)
        else:
            m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await tex.edit(f"**ERROR:** `{exc}`")
            os.remove(m_d)
            return
        U_done = f"**Uploaded on ** [Telegraph](https://telegra.ph/{media_url[0]})"
        await tex.edit(U_done)
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await tex.edit(f"**ERROR:** `{exc}`")
            return
        wow_graph = (
            f"**Uploaded as** [Telegraph](https://telegra.ph/{response['path']})"
        )
        await tex.edit(wow_graph)


add_command_help(
    "telegraph",
    [
        [
            f"tm `or` tg",
            "To upload on telegraph.",
        ],
    ],
)
