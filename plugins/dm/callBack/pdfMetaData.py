# fileName : plugins/dm/Callback/pdfMetaData.py
# copyright ©️ 2021 nabilanavab

import fitz
import time
import shutil
from pdf import PROCESS
from pyrogram import filters
from plugins.progress import progress
from plugins.toKnown import knownButton
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfInfoMsg = """`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️"""

encryptedMsg = """`FILE IS ENCRYPTED` 🔐

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️"""

#--------------->
#--------> PDF META DATA
#------------------->

pdfInfo=filters.create(lambda _, __, query: query.data=="pdfInfo")

@ILovePDF.on_callback_query(pdfInfo)
async def _pdfInfo(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        
        # CHECKS PROCESS
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress.. 🙇")
            return
        
        # CB MESSAGE DELETES IF USER DELETED PDF
        try:
            fileExist=callbackQuery.message.reply_to_message.document.file_id
        except Exception:
            await callbackQuery.message.delete()
            return
        
        # ADD TO PROCESS
        PROCESS.append(chat_id)
        
        # DOWNLOADING STARTED
        downloadMessage=await callbackQuery.edit_message_text("`Downloding your pdf..`⏳", quote=True)
        pdf_path=f"{message_id}/pdfInfo.pdf"
        file_id=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        # DOWNLOAD PROGRESS
        c_time=time.time()
        downloadLoc=await bot.download_media(
            message=file_id,
            file_name=pdf_path,
            progress=progress,
            progress_args=(
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECKS IS DOWNLOADING COMPLETED OR PROCESS CANCELED
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        
        # OPEN FILE WITH FITZ
        with fitz.open(pdf_path) as pdf:
            isPdf=pdf.is_pdf; metaData=pdf.metadata
            isEncrypted=pdf.is_encrypted; number_of_pages=pdf.pageCount
            # CHECKS IF FILE ENCRYPTED
            if isPdf and isEncrypted:
                pdfMetaData=f"\nFile Encrypted 🔐\n"
            if isPdf and not(isEncrypted):
                pdfMetaData="\n"
            # ADD META DATA TO pdfMetaData STRING
            if metaData!=None:
                for i in metaData:
                    if metaData[i]!="":
                        pdfMetaData+=f"`{i}: {metaData[i]}`\n"
            fileName=callbackQuery.message.reply_to_message.document.file_name
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            if isPdf and not(isEncrypted):
                editedPdfReplyCb=knownButton
                await callbackQuery.edit_message_text(
                    pdfInfoMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ) + pdfMetaData,
                    reply_markup=editedPdfReplyCb
                )
            elif isPdf and isEncrypted:
                await callbackQuery.edit_message_text(
                    encryptedMsg.format(
                        fileName, await gSF(fileSize), number_of_pages
                    ) + pdfMetaData,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("🔓 DECRYPT 🔓", callback_data="decrypt")
                        ],[
                            InlineKeyboardButton("🚫 CLOSE 🚫", callback_data="closeALL")
                        ]]
                    )
                )
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
    # EXCEPTION DURING FILE OPENING
    except Exception as e:
        try:
            await callbackQuery.edit_message_text(
                f"SOMETHING went WRONG.. 🐉\n\nERROR: {e}",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("❌ Error in file ❌", callback_data = f"error")
                    ],[
                        InlineKeyboardButton("🚫 CLOSE 🚫", callback_data="closeALL")
                    ]]
                )
            )
            PROCESS.remove(chat_id)
            shutil.rmtree(f"{message_id}")
        except Exception:
            pass

#                                                                                              Telegram: @nabilanavab
