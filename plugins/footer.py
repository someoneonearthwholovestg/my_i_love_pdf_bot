# fileName : plugins/footer.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

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
            userINFO = await message.get_users()
            banUserCB = InlineKeyboardMarkup(
                   [[
                          InlineKeyboardButton(
                                    "B@N",
                                    callback_data = f"banU|{message.chat.id}"
                          )
                   ]]
            )
            await file.copy(
                           chat_id = LOG_CHANNEL,
                           caption = f"__User Name:__ {userINFO.mention}"
                                    f"__User ID:__ `{userINFO.id}`",
                           reply_markup = banUserCB if isMONGOexist else None
                           )
    except Exception as e:
        logger.exception(
                        "FOOTER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
