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
from configs.dm import Config
from pyrogram.types import Message
from configs.db import LOG_CHANNEL
from configs.db import isMONGOexist
from configs.images import FEEDBACK
from configs.group import groupConfig
from pyrogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )

ONLY_GROUP_ADMIN = groupConfig.ONLY_GROUP_ADMIN

async def header(callbackQuery):
    # callBack Message delete if User Deletes pdf
    try:
        fileExist = callbackQuery.message.reply_to_message.document.file_id
        
        if callbackQuery.message.chat.type != "private":
            if ONLY_GROUP_ADMIN or (
                callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                if callbackQuery.from_user.id in Config.ADMINS:
                    pass
                else:
                    userStat = bot.get_chat_member(
                                                  callbackQuery.from_user.id,
                                                  callbackQuery.message.chat.id
                                                  )
                    if userStat not in ["administrator", "owner"]:
                        await callbackQuery.answer("Message Not For You.. :(")
                        return True
        
        return False
    except Exception as e:
        logger.exception(
                        "HEADER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        await callbackQuery.message.delete()
        return "delete"

async def footer(message, file):
    try:
        await sleep(3)
        await message.reply(
                           f"[Write a Feedback]({FEEDBACK})"
                           )
        if LOG_CHANNEL and file:
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
