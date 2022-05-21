# fileName : plugins/footer.py
# copyright ©️ 2021 nabilanavab

from asyncio import sleep
from pyrogram.types import Message
from configs.db import LOG_CHANNEL
from configs.db import isMONGOexist
from configs.images import FEEDBACK
from pyrogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )


async def footer(message, file):
    try:
        await sleep(3)
        await message.reply(
                           f"[Write a Feedback]({FEEDBACK})"
                           )
        if LOG_CHANNEL:
            userINFO=await message.get_users()
            banUserCB=InlineKeyboardMarkup(
                   [[
                          InlineKeyboardButton(
                                    "B@N",
                                    callback_data=f"banU|{message.chat.id}"
                          )
                   ]]
            )
            await file.copy(
                           chat_id=LOG_CHANNEL,
                           caption=f"__User Name:__ {userINFO.mention}"
                                   f"__User ID:__ `{userINFO.id}`",
                           reply_markup=banUserCB if isMONGOexist else None
                           )
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
