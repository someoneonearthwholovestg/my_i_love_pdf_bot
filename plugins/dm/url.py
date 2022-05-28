# fileName : plugins/dm/url.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
import time
from pdf import PROCESS
from pyrogram import filters
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from plugins.footer import footer
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# url Example: https://t.me/channel/message
#                       https://telegram.dog/nabilanavab/75
links = ["https://telegram.dog/", "https://t.me/", "https://telegram.me/"]

@ILovePDF.on_message(
                    filters.private &
                    ~filters.edited &
                    filters.incoming &
                    filters.text
                    )
async def _url(bot, message):
    try:
        await message.reply_chat_action(
                                       "typing"
                                       )
        # CHECKS IF BOT DOING ANY WORK
        if message.from_user.id in PROCESS:
            return await message.reply(
                                      text = f"WORK IN PROGRESS.. 🙇",
                                      reply_markup = InlineKeyboardMarkup(
                                            [[
                                                  InlineKeyboardButton("♻️ Refresh ♻️",
                                                          callback_data = "refreshUrl")
                                            ]]
                                     ),
                                     quote = True
                                     )
        PROCESS.append(message.from_user.id)
        msg = await message.reply(
                                 "__Started Fetching Datas..__ 🤫",
                                 quote = True
                                 )
        
        url = message.text
        # Get one or more messages from a chat by using message identifiers.
        # get_messages(chat_id, message_ids)
        c_time = time.time()
        if url.startswith(tuple(links)):
            part = url.split("/")
            if len(part) == 5:
                file = await bot.get_messages(
                                                chat_id = part[3],
                                                message_ids = int(part[4])
                                                )
                location = await bot.download_media(
                                                   message = file.document.file_id,
                                                   file_name = "pdf.pdf",
                                                   progress = progress,
                                                   progress_args = (
                                                                   file.document.file_size,
                                                                   msg,
                                                                   c_time
                                                                   )
                                                   )
                await message.reply_document(location)
    except Exception as e:
        logger.exception(
                        "URL:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(message.from_user.id)
            await msg.edit(
                          text = f"__ERROR: __`{message.chat.type} {e}`",
                          reply_markup = InlineKeyboardMarkup(
                               [[
                                     InlineKeyboardButton("🚫 Close 🚫",
                                                  callback_data="closeALL")
                               ]]
                          ))
        except Exception: pass

refreshUrl = filters.create(lambda _, __, query: query.data == "refreshUrl")

@ILovePDF.on_callback_query(refreshUrl)
async def _refreshUrl(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id in PROCESS:
            return await callbackQuery.answer(
                                             "Work in progress.. 🙇"
                                             )
        if (callbackQuery.chat.type != "private"
             ) and (callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                 return await callbackQuery.answer(
                                                  "Message Not For U 😏"
                                                  )
        await callbackQuery.answer()
        await _url(bot, callbackQuery.message.reply_to_message)
        await callbackQuery.message.delete()
    except Exception as e:
        logger.exception(
                        "BAN_USER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
