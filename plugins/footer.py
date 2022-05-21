# fileName : plugins/footer.py
# copyright ©️ 2021 nabilanavab

from asyncio import sleep
from pyrogram.types import Message
from configs.db import LOG_CHANNEL
from configs.images import isMONGOexist, FEEDBACK
from pyrogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )

banUserCB=InlineKeyboardMarkup(
                 [[
                          InlineKeyboardButton(
                                    "B@N",
                                    callback_data=f"banU|{message.chat.id}"
                          )
                 ]]
           )

async def footer(message, file):
    try:
        await sleep(3)
        await message.reply(
                           f"[Write a Feedback]({FEEDBACK})
                           )
        if LOG_CHANNEL:
            userINFO=await message.get_users()
            await file.copy(
                           chat_id=LOG_CHANNEL,
                           caption=f"__User Name:__ {userINFO.mention}"
                                   f"__User ID:__ `{userINFO.id}`",
                           reply_markup=banUserCB if isMONGOexist else None
                           )
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
