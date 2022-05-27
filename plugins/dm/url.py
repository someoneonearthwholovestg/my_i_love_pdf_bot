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
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from pyrogram import Client as ILovePDF
from plugins.footer import footer, header
from weasyprint.urls import URLFetchingError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
                                 "`Started Fetching Datas..` 🤫",
                                 quote = True
                                 )
        
        url = message.text
        
        #if "/" in message.text:
        #    fileName = "url"
        
        output_file = f"{message.message_id}.pdf"
        try:
            HTML(url = url).write_pdf(output_file)
        except URLFetchingError:
            PROCESS.remove(message.from_user.id)
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
            caption = "__url:__ {}\n__Request From__ {}".format(url, message.from_user.mention)
        else:
            caption = "__url:__ {}".format(url)
        
        # Getting thumbnail
        thumbnail, fileName = await thumbName(message, isPdfOrImg)
        if PDF_THUMBNAIL != thumbnail:
            await bot.download_media(
                                    message = thumbnail,
                                    file_name = f"{message.message_id}thumbnail.jpeg"
                                    )
            thumbnail = await formatThumb(f"{message.message_id}thumbnail.jpeg")
        
        logFile = await message.reply_document(
                                    file_name = "URL.pdf",
                                    document = open(path, "rb"),
                                    quote = True,
                                    caption = caption,
                                    thumb = thumbnail
                                    )
        os.remove(output_file); await msg.delete()
        PROCESS.remove(message.from_user.id)
        os.remove(f"{message.message_id}thumbnail.jpeg")
        await footer(message, logFile)
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
            os.remove(output_file)
        except Exception as e:
            logger.exception(
                            "URL:CAUSES %(e)s ERROR",
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
