from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

from alisu.config import prefix
from alisu.utils import commands
from alisu.utils.consts import http
from alisu.utils.localization import use_chat_lang
from alisu.utils.bot_error_log import logging_errors


@Client.on_message(filters.command("print", prefix))
@use_chat_lang()
@logging_errors
async def prints(c: Client, m: Message, strings):
    if len(m.command) == 1:
        return await m.reply_text(
            strings("print_usage"), reply_to_message_id=m.message_id
        )
    sent = await m.reply_text(strings("taking_screenshot"))
    text = m.text.split(maxsplit=1)[1]
    r = await http.get("https://api.itayki.com/print", params=dict(url=text))
    bio = BytesIO(r.read())
    bio.name: str = "screenshot.png"
    await m.reply_photo(bio)
    await sent.delete()


commands.add_command("print", "tools")
