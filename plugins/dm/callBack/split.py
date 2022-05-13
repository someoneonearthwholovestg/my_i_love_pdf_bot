# fileName : plugins/dm/callBack/split.py
# copyright ©️ 2021 nabilanavab

import time
import shutil
from pdf import PROCESS
from pyromod import listen
from pyrogram import filters
from plugins.checkPdf import checkPdf
from plugins.progress import progress
from pyrogram.types import ForceReply
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL
from PyPDF2 import PdfFileWriter, PdfFileReader
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

pdfInfoMsg="""`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️
"""

# ----- ----- ----- ----- ----- ----- ----- CALLBACK SPLITTING PDF ----- ----- ----- ----- ----- ----- -----

split=filters.create(lambda _, __, query: query.data=="split")
Ksplit=filters.create(lambda _, __, query: query.data.startswith("Ksplit|"))

splitR=filters.create(lambda _, __, query: query.data=="splitR")
splitS=filters.create(lambda _, __, query: query.data=="splitS")

KsplitR=filters.create(lambda _, __, query: query.data.startswith("KsplitR|"))
KsplitS=filters.create(lambda _, __, query: query.data.startswith("KsplitS|"))

# Split pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(split)
async def _split(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Split pdf » Pages:\n\nTotal Page Number(s):__ `unknown`",
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("With In Range 🦞", callback_data="splitR")
                ],[
                    InlineKeyboardButton("Single Page 🐛", callback_data="splitS")
                ],[
                    InlineKeyboardButton("« Back «", callback_data="BTPM")
                ]]
            )
        )
    except Exception:
        pass

# Split pgNo (with known pdf page number)
@ILovePDF.on_callback_query(Ksplit)
async def _Ksplit(bot, callbackQuery):
    try:
        _, number_of_pages=callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"Split pdf » Pages:\n\nTotal Page Number(s): {number_of_pages}__ 🌟",
            reply_markup = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("With In Range 🦞", callback_data=f"KsplitR|{number_of_pages}")
                ],[
                    InlineKeyboardButton("Single Page 🐛", callback_data=f"KsplitS|{number_of_pages}")
                ],[
                    InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                ]]
            )
        )
    except Exception:
        pass

# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(splitR)
async def _splitROrS(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        # CHECKS IF USER IN PROCESS
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress..🙇")
            return
        # ADD TO PROCESS
        PROCESS.append(chat_id); nabilanavab=True; i=0
        while(nabilanavab):
            # REQUEST FOR PG NUMBER (MAX. LIMIT 5)
            if i>=5:
                await callbackQuery.message.reply("`5 attempt over.. Process canceled..`😏")
                break
            i+=1
            needPages=await bot.ask(
                text="__Pdf Split » By Range\nNow, Enter the range (start:end) :__\n\n/exit __to cancel__",
                chat_id=chat_id, reply_to_message_id=message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            # IF /exit PROCESS CANCEL
            if needPages.text=="/exit":
                await needPages.reply("`Process Cancelled..` 😏", quote=True)
                break
            pageStartAndEnd=list(needPages.text.replace('-',':').split(':'))
            if len(pageStartAndEnd) > 2:
                await callbackQuery.message.reply("`Syntax Error: justNeedStartAndEnd `🚶")
            elif len(pageStartAndEnd)==2:
                start=pageStartAndEnd[0]; end=pageStartAndEnd[1]
                if start.isdigit() and end.isdigit():
                    if (1 <= int(pageStartAndEnd[0])):
                        if (int(pageStartAndEnd[0]) < int(pageStartAndEnd[1])):
                            nabilanavab=False
                            break
                        else:
                            await callbackQuery.message.reply("`Syntax Error: errorInEndingPageNumber `🚶")
                    else:
                        await callbackQuery.message.reply("`Syntax Error: errorInStartingPageNumber `🚶")
                else:
                    await callbackQuery.message.reply("`Syntax Error: pageNumberMustBeADigit` 🧠")
            else:
                await callbackQuery.message.reply("`Syntax Error: noEndingPageNumber Or notADigit` 🚶")
        # nabilanavab=True iff AN ERROR OCCURS
        if nabilanavab==True:
            PROCESS.remove(chat_id)
        if nabilanavab==False:
            input_file=f"{message_id}/inPut.pdf"
            output_file=f"{message_id}/outPut.pdf"
            
            downloadMessage=await callbackQuery.message.reply_text(text="`Downloding your pdf..` ⏳", quote=True)
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc=await bot.download_media(
                message=file_id, file_name=input_file, progress=progress,
                progress_args=(fileSize, downloadMessage, c_time)
            )
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            await downloadMessage.edit("`Downloading Completed..🤞`")
            checked, number_of_pages=await checkPdf(input_file, callbackQuery)
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
            splitInputPdf=PdfFileReader(input_file)
            number_of_pages=splitInputPdf.getNumPages()
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await callbackQuery.message.reply("`1st Check Number of pages` 😏")
                PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                return
            splitOutput=PdfFileWriter()
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            with open(output_file, "wb") as output_stream:
                splitOutput.write(output_stream)
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name=fileNm, thumb=PDF_THUMBNAIL, quote=True, document=output_file,
                caption=f"__from __`{pageStartAndEnd[0]}`__ to  __`{pageStartAndEnd[1]}`"
            )
            await downloadMessage.delete()
            PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
    except Exception as e:
        try:
            print("SplitR: ", e)
            PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
        except Exception:
            pass

# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(splitS)
async def _splitS(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress..🙇")
            return
        PROCESS.append(chat_id); newList=[]; nabilanavab = True; i = 0
        while(nabilanavab):
            if i>=5:
                await callbackQuery.message.reply("`5 attempt over.. Process canceled..`😏")
                break
            i+=1
            needPage=await bot.ask(
                text="__Pdf Split » By Pages\nNow, Enter Page Numbers seperate by__ (,) :\n\n/exit __to cancel__",
                chat_id=chat_id, reply_to_message_id=message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            singlePages=list(needPages.text.replace(',',':').split(':'))
            if needPages.text=="/exit":
                await needPages.reply("`Process Cancelled..` 😏")
                break
            elif 1 <= len(singlePages) <= 100:
                try:
                    for i in singlePages:
                        if i.isdigit():
                            newList.append(i)
                    if newList!=[]:
                        nabilanavab=False
                        break
                    elif newList==[]:
                        await callbackQuery.message.reply("`Cant find any number..`😏")
                        continue
                except Exception:
                    pass
            else:
                await callbackQuery.message.reply("`Something went Wrong..`😅")
        if nabilanavab==True:
            PROCESS.remove(chat_id)
        if nabilanavab==False:
            input_file=f"{message_id}/inPut.pdf"
            output_file=f"{message_id}/outPut.pdf"
            
            downloadMessage=await callbackQuery.message.reply_text(text="`Downloding your pdf..`⏳", quote=True)
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc=await bot.download_media(
                message=file_id, file_name=input_file, progress=progress,
                progress_args=(fileSize, downloadMessage, c_time)
            )
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            await downloadMessage.edit("`Downloading Completed..🤞`")
            checked, number_of_pages=await checkPdf(input_file, callbackQuery)
            if not(checked=="pass"):
                await downloadMessage.delete()
                return
            splitInputPdf=PdfFileReader(input_file)
            number_of_pages=splitInputPdf.getNumPages()
            splitOutput=PdfFileWriter()
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            with open(output_file, "wb") as output_stream:
                splitOutput.write(output_stream)
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name=fileNm, thumb=PDF_THUMBNAIL, document=output_file,
                caption=f"__Pages: __`{newList}`", quote=True
            )
            await downloadMessage.delete(); PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
    except Exception as e:
        try:
            await downloadMessage.edit(e); print("splitS ;", e); PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
        except Exception:
            pass

# Split (with known pdf page number)
@ILovePDF.on_callback_query(KsplitR)
async def _KsplitR(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress..🙇")
            return
        _, number_of_pages=callbackQuery.data.split("|")
        number_of_pages=int(number_of_pages)
        PROCESS.append(chat_id); nabilanavab=True; i=0
        while(nabilanavab):
            if i>=5:
                await callbackQuery.message.reply("`5 attempt over.. Process canceled..`😏")
                break
            i+=1
            needPages=await bot.ask(
                text=f"__Pdf Split » By Range\nNow, Enter the range (start:end) :\nTotal Pages : __`{number_of_pages}` 🌟\n\n/exit __to cancel__",
                chat_id=chat_id, reply_to_message_id=message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            if needPages.text == "/exit":
                await callbackQuery.message.reply("`Process Cancelled..` 😏")
                break
            pageStartAndEnd=list(needPages.text.replace('-',':').split(':'))
            if len(pageStartAndEnd) > 2:
                await callbackQuery.message.reply("`Syntax Error: justNeedStartAndEnd `🚶")
            elif len(pageStartAndEnd)==2:
                start = pageStartAndEnd[0]
                end = pageStartAndEnd[1]
                if start.isdigit() and end.isdigit():
                    if (int(1) <= int(start) and int(start) < number_of_pages):
                        if (int(start) < int(end) and int(end) <= number_of_pages):
                            nabilanavab = False
                            break
                        else:
                            await callbackQuery.message.reply("`Syntax Error: errorInEndingPageNumber `🚶")
                    else:
                        await callbackQuery.message.reply("`Syntax Error: errorInStartingPageNumber `🚶")
                else:
                    await callbackQuery.message.reply("`Syntax Error: pageNumberMustBeADigit` 🚶")
            else:
                await callbackQuery.message.reply("`Syntax Error: noSuchPageNumbers` 🚶")
        if nabilanavab==True:
            PROCESS.remove(chat_id)
        if nabilanavab==False:
            input_file=f"{message_id}/inPut.pdf"
            output_file=f"{message_id}/outPut.pdf"
            
            downloadMessage=await callbackQuery.message.reply_text(text="`Downloding your pdf..` ⏳", quote=True)
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc=await bot.download_media(
                message=file_id, file_name=input_file, progress=progress,
                progress_args=(fileSize, downloadMessage, c_time)
            )
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            await downloadMessage.edit("`Downloading Completed..🤞`")
            splitInputPdf=PdfFileReader(input_file)
            number_of_pages=splitInputPdf.getNumPages()
            if not(int(pageStartAndEnd[1]) <= int(number_of_pages)):
                await callbackQuery.message.reply("`1st Check the Number of pages` 😏")
                PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
                return
            splitOutput=PdfFileWriter()
            for i in range(int(pageStartAndEnd[0])-1, int(pageStartAndEnd[1])):
                splitOutput.addPage(
                    splitInputPdf.getPage(i)
                )
            with open(output_file, "wb") as output_stream:
                splitOutput.write(output_stream)
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name=fileNm, thumb=PDF_THUMBNAIL, quote=True, document=output_file,
                caption=f"__from __`{pageStartAndEnd[0]}`__ to  __`{pageStartAndEnd[1]}`"
            )
            await downloadMessage.delete(); PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
    except Exception as e:
        try:
            print("KsplitR :", e); PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
        except Exception:
            pass

# Split (with unknown pdf page number)
@ILovePDF.on_callback_query(KsplitS)
async def _KsplitS(bot, callbackQuery):
    try:
        chat_id=callbackQuery.message.chat.id
        message_id=callbackQuery.message.message_id
        if chat_id in PROCESS:
            await callbackQuery.answer("Work in progress..🙇")
            return
        PROCESS.append(chat_id)
        _, number_of_pages=callbackQuery.data.split("|")
        newList=[]; nabilanavab=True; i=0
        while(nabilanavab):
            if i>=5:
                await callbackQuery.message.reply("`5 attempt over.. Process canceled..`😏")
                break
            i+=1
            needPages=await bot.ask(
                text=f"__Pdf Split » By Pages\nEnter Page Numbers seperate by__ (,) :\n__Total Pages : __`{number_of_pages}` 🌟\n\n/exit __to cancel__",
                chat_id=chat_id, reply_to_message_id=message_id,
                filters=filters.text, reply_markup=ForceReply(True)
            )
            singlePages=list(needPages.text.replace(',',':').split(':'))
            if needPages.text=="/exit":
                await needPages.reply("`Process Cancelled..` 😏")
                break
            elif 1 <= int(len(singlePages)) and int(len(singlePages)) <= 100:
                try:
                    for i in singlePages:
                        if (i.isdigit() and int(i) <= int(number_of_pages)):
                            newList.append(i)
                    if newList == []:
                        await needPages.reply(f"`Enter Numbers less than {number_of_pages}..`😏")
                        # continue
                    else:
                        nabilanavab = False
                        break
                except Exception:
                    pass
            else:
                await callbackQuery.message.reply("`Something went Wrong..`😅")
        if nabilanavab==True:
            PROCESS.remove(chat_id)
        if nabilanavab==False:
            input_file=f"{message_id}/inPut.pdf"
            output_file=f"{message_id}/outPut.pdf"
            
            downloadMessage=await callbackQuery.message.reply_text(text="`Downloding your pdf..`⏳", quote=True)
            file_id=callbackQuery.message.reply_to_message.document.file_id
            fileSize=callbackQuery.message.reply_to_message.document.file_size
            c_time=time.time()
            downloadLoc=await bot.download_media(
                message=file_id, file_name=input_file, progress=progress,
                progress_args=(fileSize, downloadMessage, c_time)
            )
            if downloadLoc is None:
                PROCESS.remove(chat_id)
                return
            await downloadMessage.edit("`Downloading Completed..🤞`")
            splitInputPdf=PdfFileReader(input_file)
            number_of_pages=splitInputPdf.getNumPages()
            splitOutput=PdfFileWriter()
            for i in newList:
                if int(i) <= int(number_of_pages):
                    splitOutput.addPage(
                        splitInputPdf.getPage(
                            int(i)-1
                        )
                    )
            with open(output_file, "wb") as output_stream:
                splitOutput.write(output_stream)
            fileNm=callbackQuery.message.reply_to_message.document.file_name
            await callbackQuery.message.reply_chat_action("upload_document")
            await callbackQuery.message.reply_document(
                file_name=fileNm, thumb=PDF_THUMBNAIL, document=output_file,
                caption=f"__Pages: __`{newList}`", quote=True
            )
            await downloadMessage.delete(); PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
    except Exception as e:
        try:
            await downloadMessage.edit(e); print("Ksplits: ", e); PROCESS.remove(chat_id); shutil.rmtree(f"{message_id}")
        except Exception:
            pass

#                                                                                                                                    Telegram: @nabilanavab
