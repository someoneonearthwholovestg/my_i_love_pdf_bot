# fileName : plugins/dm/callBack/watermark.py
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
import fitz
import shutil
import asyncio
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from configs.dm import Config
from plugins.thumbName import (
                              thumbName,
                              formatThumb
                              )
from plugins.checkPdf import checkPdf
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from plugins.footer import footer, header
from plugins.progress import progress, uploadProgress
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

wa = filters.create(lambda _, __, query: query.data in ["wa", "Kwa"])

@ILovePDF.on_callback_query(wa)
async def _watermarkPDF(bot, callbackQuery):
    try:
        if await header(bot, callbackQuery):
            return
        
        chat_id = callbackQuery.message.chat.id
        message_id = callbackQuery.message.message_id
        
        # CHECK IF BOT DOING ANY WORK
        if chat_id in PROCESS:
            return await callbackQuery.answer(
                                             "Work in progress..🙇"
                                             )
        await callbackQuery.answer("⚙️ PROCESSING..")
        # ADD TO PROCESS         # DATA
        PROCESS.append(chat_id)  ;data = callbackQuery.data
        fileId = callbackQuery.message.reply_to_message.document.file_id
        fileSize = callbackQuery.message.reply_to_message.document.file_size
        fileNm = callbackQuery.message.reply_to_message.document.file_name
        _, fileExt = os.path.splitext(fileNm)        # seperates name & extension
        nabilanavab = True: i = 0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i >= 5:
                await callbackQuery.message.reply(
                                                 "`5 attempt over.. Process canceled..`😏"
                                                 )
                break
            i += 1
            askWA = await bot.ask(
                                 text = "__Send me the watermark Image as file.__"
                                        "__ Supported Files [png, jpeg, jpg]__",
                                 chat_id = chat_id,
                                 reply_to_message_id = message_id,
                                 filters = None
                                 )
            # IF /exit PROCESS CANCEL
            if askWA.text == "/exit":
                await askWA.reply(
                                 "`Process Cancelled..` 😏",
                                 quote = True
                                 )
                break
            if askWA.document:
                waFile = askWA.document.file_name
                _, waExt = os.path.splitext(waFile)
                if waExt.lower() in [".png", ".jpeg", ".jpg"]:
                    waSize = askWA.document.file_size
                    waID = askWA.document.file_id
                    nabilanavab = False
                    break
        
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab == True:
            PROCESS.remove(chat_id)
        # GET /merge, REACHES MAX FILE SIZE OR MAX NO OF PDF
        if nabilanavab == False:
            # START DOWNLOAD
            downloadMessagedownloadMessage = await callbackQuery.message.reply_text(
                                                                                   "`Downloding your pdf..` 📥", 
                                                                                   quote = True
                                                                                   )
            c_time = time.time()
            input_file = await bot.download_media(
                                                 message = fileId,
                                                 file_name = f"{message_id}/inPut.pdf",
                                                 progress = progress,
                                                 progress_args = (
                                                                 fileSize,
                                                                 downloadMessage,
                                                                 c_time
                                                                 )
                                                 )
            # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
            if input_file is None:
                PROCESS.remove(chat_id)
                return
            # CHECKS PDF CODEC, ENCRYPTION..
            if data != "Kwa":
                checked, noOfPg = await checkPdf(
                                                input_file,
                                                callbackQuery
                                                )
            await downloadMessage.edit(
                                      "__Getting watermark File..__ 🙄"
                                      )
            c_time = time.time()
            wa_file = await bot.download_media(
                                              message = waID,
                                              file_name = f"{message_id}/watermarkPDF.{waExt}",
                                              progress = progress,
                                              progress_args = (
                                                              waSize,
                                                              downloadMessage,
                                                              c_time
                                                              )
                                              )
            if wa_file is None:
                await downloadMessage.edit("Something went Wrong 🙂")
                PROCESS.remove(chat_id)
                shutil.rmtree(f"{message_id}")
                return
            # MERGING STARTED
            await downloadMessage.edit(
                                      "Adding watermark to PDF File 💩"
                                      )
            output_pdf = f"{message_id}/outPut.pdf"
            
            # define the position (upper-right corner)
            image_rectangle = fitz.Rect(450,20,550,120)
            
            # retrieve the first page of the PDF
            file_handle = fitz.open(input_file)
            first_page = file_handle[0]
            
            # add the image
            first_page.insertImage(
                                  image_rectangle,
                                  fileName = wa_file
                                  )
            
            file_handle.save(output_pdf)
            
            # Getting thumbnail
            thumbnail, fileName = await thumbName(callbackQuery.message, fileNm)
            if PDF_THUMBNAIL != thumbnail:
                location = await bot.download_media(
                                                   message = thumbnail,
                                                   file_name = f"{message_id}.jpeg"
                                                   )
                thumbnail = await formatThumb(location)
            
            await downloadMessage.edit(
                                      "`Started Uploading..` 📤"
                                      )
            await callbackQuery.message.reply_chat_action(
                                                         "upload_document"
                                                         )
            c_time = time.time()
            # SEND DOCUMENT
            with open(output_pdf, "rb") as outPut:
                await askPDF.reply_document(
                                           file_name = fileName,
                                           quote = True,
                                           document = output_pdf,
                                           thumb = thumbnail,
                                           caption = "`Watermark PDF 🙂`",
                                           progress = uploadProgress,
                                           progress_args = (
                                                           downloadMessage,
                                                           c_time
                                                           )
                                           )
            await downloadMessage.delete()
            try:
                os.remove(location)
            except Exception: pass
            shutil.rmtree(f"{message_id}")
            PROCESS.remove(chat_id)
            await footer(callbackQuery.message, False)
    except Exception as e:
        logger.exception(
                        "MERGE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            shutil.rmtree(f"{message_id}")
            PROCESS.remove(chat_id)
            os.remove(location)
        except Exception:
            pass

#                                                                                            Telegram: @nabilanavab
