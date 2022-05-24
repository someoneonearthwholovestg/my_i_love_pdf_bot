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
from pdf import PROCESS
from weasyprint import HTML
from pyrogram import filters
from pyrogram import Client as ILovePDF
from weasyprint.urls import URLFetchingError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@ILovePDF.on_message(
                    filters.private &
                    ~filters.edited &
                    filters.incoming &
                    filters.text.startswith("https")
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
                                 "`Started Fetching Datas..` 🤫",
                                 quote = True
                                 )
        
        if (message.chat.id != "private") and (message.reply_to_message.text):
            url = message.reply_to_message.text
        else:
            url = message.text
        
        if "/" in message.text:
            if message.text.split("/")[4]:
                fileName = message.text.split("/")[4]
            elif message.text.split("/")[3]:
                fileName = message.text.split("/")[3]
            elif message.text.split("/")[2]:
                fileName = message.text.split("/")[2]
            else:
                fileName = "url"
        
        output_file = f"{message.message_id}.pdf"
        try:
            HTML(url = url).write_pdf(output_file)
        except URLFetchingError:
            PROCESS.return(message.from_user.id)
            os.remove(output_file)
            return await msg.edit(
                                 "Unable to reach your web page"
                                 )
        
        await msg.edit(
                      "`Now Started Uploading..` 😉"
                      )
        await message.reply_chat_action(
                                       "upload_document"
                                       )
        
        if message.chat.type in ["group", "supergroup"]:
            caption = "__url:__ {}"
                      "__Request From__ {}".format(
                                                  url,
                                                  message.from_user.mention
                                                  )
        else:
            caption = "__url:__ {}".format(url)
        
        await message.reply_document(
                                    file_name = "URL.pdf",
                                    document = open(path, "rb"),
                                    quote = True,
                                    caption = caption,
                                    thumb = PDF_THUMBNAIL
                                    )
        os.remove(output_file); await msg.delete()
        PROCESS.remove(message.from_user.id)
    except Exception as e:
        logger.exception(
                        "BAN_USER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            PROCESS.remove(message.from_user.id)
            await msg.edit(
                          text = f"__ERROR: __`{e}`",
                          reply_markup = InlineKeyboardMarkup(
                               [[
                                     InlineKeyboardButton("🚫 Close 🚫",
                                                  callback_data="closeALL")
                               ]]
                          ))
            os.remove(output_file)
        except Exception as e:
            logger.exception(
                            "BAN_USER:CAUSES %(e)s ERROR",
                            exc_info=True
                            )

refreshUrl = filters.create(lambda _, __, query: query.data == "refreshUrl")

@ILovePDF.on_callback_query(refreshUrl)
async def _refreshUrl(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id in PROCESS:
            return await callbackQuery.answer(
                                             "Work in progress.. 🙇"
                                             )
        if (callbackQuery.message.chat.type != "private"
             ) and (callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
                 return await callbackQuery.answer(
                                                  "Message Not For U 😏"
                                                  )
        await _url(bot, callbackQuery.message.reply_to_message)
        await callbackQuery.message.delete()
    except Exception as e:
        logger.exception(
                        "BAN_USER:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                  Telegram: @nabilanavab
