# fileName : plugins/dm/generate.py
# copyright ©️ 2021 nabilanavab

import os
import shutil
import asyncio
from pdf import PDF
from pyrogram import filters
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL

#--------------->
#--------> LOCAL VARIABLES
#------------------->

feedbackMsg="[Write a feedback 📋](https://t.me/ILovePDF_bot)"

#--------------->
#--------> REPLY TO /generate MESSAGE
#------------------->

@ILovePDF.on_message(filters.private & filters.command(["generate"]) & ~filters.edited)
async def generate(bot, message):
    try:
        chat_id=message.chat.id
        # newName : new file name(/generate ___)
        newName=str(message.text.replace("/generate", ""))
        images=PDF.get(chat_id)
        if isinstance(images, list):
            pgnmbr=len(PDF[chat_id])
            del PDF[chat_id]
        
        # IF NO IMAGES SEND BEFORE
        if not images:
            await message.reply_chat_action("typing")
            imagesNotFounded=await message.reply_text("`No image founded.!!`😒")
            await asyncio.sleep(5); await message.delete()
            await imagesNotFounded.delete()
            return
        gnrtMsgId=await message.reply_text(f"`Generating pdf..`💚")
        
        if newName==" name":
            fileName=f"{message.from_user.first_name}"+".pdf"
        elif len(newName) > 1 and len(newName) <= 45:
            fileName=f"{newName}"+".pdf"
        elif len(newName) > 45:
            fileName=f"{message.from_user.first_name}"+".pdf"
        else:
            fileName=f"{chat_id}"+".pdf"
        
        filePath=f"{message.chat.id}.pdf"
        images[0].save(filePath, save_all=True, append_images=images[1:])
        await gnrtMsgId.edit("`Uploading pdf.. `🏋️")
        await message.reply_chat_action("upload_document")
        with open(filePath, "rb") as pdf:
            generated=await message.reply_document(
                file_name=fileName, document=pdf, thumb=PDF_THUMBNAIL,
                caption=f"file Name: `{fileName}`\n`Total pg's: {pgnmbr}`"
            )
        await gnrtMsgId.edit("`Successfully Uploaded.. `🤫")
        shutil.rmtree(f"{chat_id}"); await asyncio.sleep(5)
        await message.reply_chat_action("typing")
        await message.reply_text(feedbackMsg, disable_web_page_preview=True)
    except Exception:
        try:
            shutil.rmtree(f"{chat_id}")
        except Exception:
            pass

#                                                                                  Telegram: @nabilanavab
