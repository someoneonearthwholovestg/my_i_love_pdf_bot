# fileName : plugins/dm/id.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from pyrogram import Client as ILovePDF

#--------------->
#--------> LOCAL VARIABLES
#------------------->

feedbackMsg = "[Write a feedback 📋](https://t.me/ilovepdf_bot)"

#--------------->
#--------> GET USER ID (/id)
#------------------->

@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["id"]))
async def userId(bot, message):
    try:
        await message.reply_text(f'Your Id: `{message.chat.id}`', quote=True)
    except Exception:
        pass

@ILovePDF.on_message(filters.private & filters.command(["feedback"]) & ~filters.edited)
async def feedback(bot, message):
    try:
        await message.reply_text(feedbackMsg, disable_web_page_preview=True)
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
