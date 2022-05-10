# fileName : plugins/dm/callBack/pdfManupulator.py
# copyright ©️ 2021 nabilanavab

import os
import time
import shutil
import asyncio
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from Configs.dm import Config
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Importing Pdf Process Funs.
from plugins.dm.callBack.encrypt import encryptPDF
from plugins.dm.callBack.decrypt import decryptPDF
from plugins.dm.callBack.compress import compressPDF
from plugins.dm.callBack.pdfFormatter import formatterPDF

# checks if ocr works (nabilanavab==False)
from plugins.dm.callBack.ocr import nabilanavab
if nabilanavab==False:
    from plugins.dm.callBack.ocr import ocrPDF

#--------------->
#--------> LOCAL VARIABLES
#------------------->

PDF_THUMBNAIL=Config.PDF_THUMBNAIL

cancelBtn=InlineKeyboardMarkup([[InlineKeyboardButton("« Cancel »", callback_data="closeme")]])

#--------------->
#--------> PYRO FILTERS
#------------------->

pdfInfo=filters.create(lambda _, __, query: query.data.startswith("KpdfInfo"))
ocr=filters.create(lambda _, __, query: query.data.startswith(tuple(["ocr", "Kocr"])))
compress=filters.create(lambda _, __, query: query.data in ["compress", "Kcompress"])
decrypt=filters.create(lambda _, __, query: query.data.startswith(tuple(["decrypt", "Kdecrypt"])))
encrypt=filters.create(lambda _, __, query: query.data.startswith(tuple(["encrypt", "Kencrypt"])))
formatter=filters.create(lambda _, __, query: query.data.startswith(tuple(["format", "Kformat"])))

#--------------->
#--------> CALLBACK QUERY
#------------------->

@ILovePDF.on_callback_query(pdfInfo | ocr | compress | decrypt | encrypt | formatter)
async def _pdfManupulator(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        
        # Never Work OCR if nabilanavab==True
        # Deploy From Docker Files (else OCR never works)
        if callbackQuery.data.startswith(tuple(["ocr", "Kocr"])):
            if nabilanavab:
                await callbackQuery.answer("Owner Restricted 😎🤏")
                return
            if data[0]=="K":
                _, number_of_pages=callbackQuery.data.split("|")
                if int(number_of_pages)>=5:
                    await callbackQuery.answer("send a pdf file less than 5 pages.. 🙄")
                    return
        
        # PDF A4 Formatter
        if callbackQuery.data.startswith(tuple(["Kformat"])):
            _, number_of_pages=callbackQuery.data.split("|")
            if int(number_of_pages)>=5:
                await callbackQuery.answer("send a pdf file less than 5 pages.. 🙄")
                return
        
        # Known MetaData
        if callbackQuery.data.startswith("KpdfInfo"):
            _, number_of_pages=callbackQuery.data.split("|")
            await callbackQuery.answer("Total {} pages.. 🐾".format(number_of_pages))
            return
        
        # callBack Message delete if User Deletes pdf
        try:
            fileExist=callbackQuery.message.reply_to_message.document.file_id
        except Exception:
            await callbackQuery.message.delete()
            return
        
        # CHECKS IF BOT DOING ANY WORK
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress.. 🙇")
            return
        
        # ↓ ADD TO PROCESS       ↓ CALLBACK DATA
        PROCESS.append(chat_id); data=callbackQuery.data
        
        if data[0]=="K":
            _, number_of_pages=callbackQuery.data.split("|")
        
        # Asks password for encryption, decryption
        if data.startswith(tuple(["decrypt", "Kdecrypt", "encrypt", "Kencrypt"])):
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            password=await bot.ask(
                chat_id=chat_id, reply_to_message_id=message_id,
                text="__PDF Decryption »\nNow, please enter the password :__\n\n/exit __to cancel__",
                filters=filters.text, reply_markup=ForceReply(True)
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if password.text=="/exit":
                await password.reply("`process canceled.. `😏", quote=True)
                PROCESS.remove(chat_id)
                return
        
        # fileNm continues false(if not rename) and take org. name as fileName
        fileNm=False
        # Asks newFile Name [renamePdf]
        if data.startswith(tuple(["rename", "Krename"])):
            # PYROMOD ADD-ON (ASK'S PASSWORD)
            newName=await bot.ask(
                chat_id=chat_id, reply_to_message_id=message_id,
                text="__Rename PDF »\nNow, please enter the new name:__\n\n/exit __to cancel__",
                filters=filters.text, reply_markup=ForceReply(True)
            )
            # CANCEL DECRYPTION PROCESS IF MESSAGE == /exit
            if newName.text=="/exit":
                await password.reply("`process canceled.. `😏", quote=True)
                PROCESS.remove(chat_id)
                return
            else:
                if newName.text[-4:]==".pdf":
                    fileNm=newName[-4:]
                else:
                    fileNm=newName.text+".pdf"
        
        # DOWNLOAD MESSSAGE
        downloadMessage=await callbackQuery.message.reply_text(
            "`Downloding your pdf..` ⏳", reply_markup=cancelBtn, quote=True
        )
        input_file=f"{message_id}/inPut.pdf"
        output_file=f"{message_id}/outPut.pdf"
        file_id=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        if not fileNm:
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
        
        # STARTED DOWNLOADING
        c_time=time.time()
        downloadLoc=await bot.download_media(
            message=file_id,
            file_name=input_file,
            progress=progress,
            progress_args=(
                fileSize,
                downloadMessage,
                c_time
            )
        )
        # CHECKS PDF DOWNLOADED OR NOT
        if downloadLoc is None:
            PROCESS.remove(chat_id)
            return
        await downloadMessage.edit("⚙️`Started Processing..`", reply_markup=cancelBtn)
        # CHECK PDF OR NOT(HERE compressed, SO PG UNKNOWN)
        if data[0]!='K':
            # check file encryption, codec.
            checked, number_of_pages=await checkPdf(input_file, callbackQuery)
            if data.startswith("decrypt"):
                if not(checked=="encrypted"):
                    await downloadMessage.edit("File Not Encrypted..🙏🏻")
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            else:
                if not(checked=="pass"):
                    await downloadMessage.delete()
                    return
        
        if chat_id in PROCESS:
            if data in ["compress", "Kcompress"]:
                await downloadMessage.edit("Started Compressing.. 🌡️", reply_markup=cancelBtn)
                caption=await compressPDF(downloadMessage, message_id)
                await downloadMessage.edit(f"{caption}", reply_markup=cancelBtn)
                if caption==False:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data.startswith(tuple(["decrypt", "Kdecrypt"])):
                await downloadMessage.edit("Started Decrypting.. 🔓", reply_markup=cancelBtn)
                caption=await decryptPDF(downloadMessage, message_id, password)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data.startswith(tuple(["encrypt", "Kencrypt"])):
                await downloadMessage.edit("Started Encrypting.. 🔐", reply_markup=cancelBtn)
                caption=await encryptPDF(downloadMessage, message_id, password)
                if not caption:
                    PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                    return
            if data.startswith(tuple(["ocr", "Kocr"])):
                if number_of_pages>5:
                    await downloadMessage.edit("__Send me a file less than 5 images__ 😅")
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
                else:
                    await downloadMessage.edit("Adding OCR Layer.. ✍️", reply_markup=cancelBtn)
                    caption=await ocrPDF(downloadMessage, message_id)
                    if not caption:
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
            if data.startswith(tuple(["format", "Kformat"])):
                if number_of_pages>5:
                    await downloadMessage.edit("__Send me a file less than 5 images__ 😅")
                    PROCESS.remove(chat_id)
                    shutil.rmtree(f"{message_id}")
                    return
                else:
                    await downloadMessage.edit("Started Formatting.. 🤘", reply_markup=cancelBtn)
                    caption=await formatterPDF(downloadMessage, message_id)
                    if not caption:
                        PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                        return
            if data.startswith(tuple(["rename", "Krename"])):
                await downloadMessage.edit("Renameing PDf.. ✏️", reply_markup=cancelBtn)
                asyncio.sleep(3)
        else:
            shutil.rmtree(f"{message_id}")
            return
        
        await callbackQuery.message.reply_chat_action("upload_document")
        await downloadMessage.edit("`Started Uploading..` 🏋️", reply_markup=cancelBtn)
        await callbackQuery.message.reply_document(
            file_name=f"{fileNm}.pdf", quote=True,
            document=open(output_file, "rb"), thumb=PDF_THUMBNAIL,
            caption=caption
        )
        await downloadMessage.delete()
        PROCESS.remove(chat_id)
        shutil.rmtree(f"{message_id}")
    except Exception as e:
        try:
            downloadMessage.edit(e)
            print("plugins/dm/callBack/pdfManupulator: " , e)
            shutil.rmtree(f"{message_id}")
            PROCESS.remove(chat_id)
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
