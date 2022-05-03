# fileName : plugins/dm/waste.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup


#--------------->
#--------> PDF REPLY BUTTON
#------------------->

@ILovePDF.on_message(filters.private & ~filters.edited)
async def spam(bot, message):
    try:
        await message.reply_chat_action("typing")
        await message.reply_text(
            f"`no one gonna to help you` 😏", quote=True
        )
    except Exception:
        pass

#                                                     Telegram: @nabilanavab
