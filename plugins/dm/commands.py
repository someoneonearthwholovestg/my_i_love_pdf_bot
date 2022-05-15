# fileName : plugins/dm/commands.py
# copyright ©️ 2021 nabilanavab

import os
import shutil
from pdf import PDF
from pdf import PROCESS
from pyrogram import filters
from pyrogram import Client as ILovePDF


feedbackMsg="[Write a feedback 📋](https://t.me/ilovepdf_bot)"


# ❌ CANCELS CURRENT PDF TO IMAGES WORK ❌
@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["cancel"]))
async def cancelP2I(bot, message):
    try:
        PROCESS.remove(message.chat.id)
        await message.delete()          # delete /cancel if process canceled
    except Exception:
        try:
            await message.reply_chat_action("typing")
            await message.reply_text('🤔', quote=True)
        except Exception:
            pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message(filters.command(["delete"]))
async def _cancelI2P(bot, message):
    try:
        await message.reply_chat_action("typing")
        del PDF[message.chat.id]
        await message.reply_text("`Queue deleted Successfully..`🤧", quote=True)
        shutil.rmtree(f"{message.chat.id}")
    except Exception:
        await message.reply_text("`No Queue founded..`😲", quote=True)

# ❌ GET USER ID (/id) ❌
@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["id"]))
async def userId(bot, message):
    try:
        await message.reply_text(f'Your Id: `{message.chat.id}`', quote=True)
    except Exception:
        pass

# ❌ GET FEEDBACK MESSAGE ❌
@ILovePDF.on_message(filters.private & filters.command(["feedback"]) & ~filters.edited)
async def feedback(bot, message):
    try:
        await message.reply_text(feedbackMsg, disable_web_page_preview=True)
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab