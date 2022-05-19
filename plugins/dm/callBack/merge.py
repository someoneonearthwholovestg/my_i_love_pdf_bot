# fileName : plugins/dm/callBack/merge.py
# copyright ©️ 2021 nabilanavab

import os
import time
import shutil
import asyncio
from pyromod import listen
from pyrogram import filters
from configs.dm import Config
from PyPDF2 import PdfFileMerger
from configs.global import PROCESS
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

MERGE={}; MERGEsize={}

if Config.MAX_FILE_SIZE:
    MAX_FILE_SIZE=int(os.getenv("MAX_FILE_SIZE"))
    MAX_FILE_SIZE_IN_kiB=MAX_FILE_SIZE * (10**6)
else:
    MAX_FILE_SIZE=False

#--------------->
#--------> MERGE PDFS
#------------------->

merge=filters.create(lambda _, __, query: query.data == "merge")

@ILovePDF.on_callback_query(merge)
async def _merge(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        
        # CHECK IF BOT DOING ANY WORK
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress..🙇")
            return
        # ADD TO PROCESS
        PROCESS.append(chat_id)
        fileId=callbackQuery.message.reply_to_message.document.file_id
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        fileNm=callbackQuery.message.reply_to_message.document.file_name
        fileNm, fileExt=os.path.splitext(fileNm)        # seperates name & extension
        # ADDING FILE ID & SIZE TO MERGE, MERGEsize LIST (FOR FUTURE USE)
        MERGE[chat_id]=[fileId]; MERGEsize[chat_id]=[fileSize]
        # REQUEST FOR OTHER PDFS FOR MERGING
        nabilanavab=True; size=0
        while(nabilanavab):
            if len(MERGE[chat_id]) >= 5:
                await callbackQuery.message.reply(
                    "__Due to Overload you can only merge 5 pdfs at a time__", quote=True
                )
                nabilanavab=False
                break
            askPDF=await bot.ask(
                text="__MERGE pdfs » Total pdfs in queue: {}__\n\n/exit __to cancel__\n/merge __to merge__".format(
                    len(MERGE[chat_id])
                ),
                chat_id=chat_id, reply_to_message_id=message_id, filters=None
            )
            if askPDF.text=="/exit":
                await askPDF.reply(
                    "`Process Cancelled..` 😏", quote=True
                )
                PROCESS.remove(chat_id); del MERGE[chat_id]; del MERGEsize[chat_id]
                break
            if askPDF.text=="/merge":
                nabilanavab=False
                break
            # IS SEND MESSAGE A DOCUMENT
            if askPDF.document:
                file_id=askPDF.document.file_id
                file_size=askPDF.document.file_size
                # CHECKING FILE EXTENSION .pdf OR NOT
                if fileExt==".pdf":
                    # CHECKING TOTAL SIZE OF MERGED PDF
                    for _ in MERGEsize[chat_id]:
                        size = int(_) + size
                    # CHECKS MAXIMUM FILE SIZE (IF ADDED) ELSE 1.8 GB LIMIT
                    if (MAX_FILE_SIZE and MAX_FILE_SIZE_IN_kiB <= int(size)) or int(size) >= 1800000000:
                        await callbackQuery.message.reply(
                            f"`Due to Overload Bot Only Support %sMb pdfs..`😐"%(MAX_FILE_SIZE if MAX_FILE_SIZE else "1.8Gb")
                        )
                        nabilanavab=False
                        break
                    # ADDING NEWLY ADDED PDF FILE ID & SIZE TO LIST
                    MERGE[chat_id].append(file_id)
                    MERGEsize[chat_id].append(file_size)
        # nabilanavab=True ONLY IF PROCESS CANCELLED
        if nabilanavab==True:
            PROCESS.remove(chat_id)
        # GET /merge, REACHES MAX FILE SIZE OR MAX NO OF PDF
        if nabilanavab==False:
            # DISPLAY TOTAL PDFS FOR MERGING
            downloadMessage=await askPDF.reply_text(
                f"`Total PDF's : {len(MERGE[chat_id])}`.. 💡", quote=True)
            asyncio.sleep(.5); i=0
            # ITERATIONS THROUGH FILE ID'S AND DOWNLOAD
            for iD in MERGE[chat_id]:
                await downloadMessage.edit(
                    f"__Started Downloading Pdf :{i+1}__"
                )
                # START DOWNLOAD
                c_time=time.time()
                downloadLoc=await bot.download_media(
                    message=iD, file_name=f"merge{chat_id}/{i}.pdf", progress=progress,
                    progress_args=(
                        MERGEsize[chat_id][i], downloadMessage, c_time
                    )
                )
                # CHECKS IF DOWNLOAD COMPLETE/PROCESS CANCELLED
                if downloadLoc is None:
                    PROCESS.remove(chat_id)
                    await callbackQuery.message.reply_text(
                        "`Merge Process Cancelled.. 😏`", quote=True
                    )
                    shutil.rmtree(f"merge{chat_id}")
                    return
                # CHECKS PDF CODEC, ENCRYPTION..
                checked, noOfPg=await checkPdf(f"merge{chat_id}/{i}.pdf", callbackQuery)
                # REMOVE FILE FROM DIRECTORY IF FILE NOT ENCRYPTED OR CODECERROR
                if not(checked=="pass"):
                    os.remove(f"merge{chat_id}/{i}.pdf")
                i += 1
            directory=f'merge{chat_id}'
            pdfList=[os.path.join(directory, file) for file in os.listdir(directory)]
            # SORT DIRECTORY PATH BY ITS MODIFIED TIME
            pdfList.sort(key=os.path.getctime)
            numbPdf=len(pdfList)
            # MERGING STARTED
            await downloadMessage.edit("__Merging Started.. __ 🪄")
            output_pdf=f"merge{chat_id}/merge.pdf"
            #PyPDF 2
            merger=PdfFileMerger()
            for i in pdfList:
                merger.append(i)
            merger.write(output_pdf)
            # STARTED UPLOADING
            await downloadMessage.edit("`Started Uploading..`🏋️")
            await callbackQuery.message.reply_chat_action("upload_document")
            # SEND DOCUMENT
            with open(output_pdf, "rb") as outPut:
                await askPDF.reply_document(
                    file_name=f"{fileNm}.pdf", quote=True,
                    document=outPut, thumb=PDF_THUMBNAIL,
                    caption="__merged pdf__"
                )
            await downloadMessage.delete()
            shutil.rmtree(f"merge{chat_id}"); PROCESS.remove(chat_id)
    except Exception as e:
        try:
            print("plugins/dm/callback/merge: ", e)
            shutil.rmtree(f"merge{chat_id}"); PROCESS.remove(chat_id)
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
