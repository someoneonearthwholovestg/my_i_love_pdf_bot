# fileName : plugins/dm/commands.py
# copyright ©️ 2021 nabilanavab

import os
import shutil
from pdf import PDF
from pdf import PROCESS
from asyncio import sleep
from pyrogram import filters
from configs.images import FEEDBACK
from configs.dm.Config import ADMINS
from pyrogram import Client as ILovePDF


feedbackMsg=f"[Write a feedback 📋]({FEEDBACK})"

userHELP="""[USER COMMAND MESSAGES]:\n
         /start, /ping: to check whether Bot alive\n
         /help, /command: for this message\n
         /generate: generate PDF with current images\n
         /delete: deletes the current image to pdf queue\n
         /txt2pdf: to create pdf files from text message\n
         /feedback: to Write something about i💜PDF bot"""
adminHelp="""\n\n[ADMIN COMMAND MESSAGES]:\n
          /server: to get current bot, server status\n
          /ban `id/usrnm`: to ban a user\n
          /unban `id/usrnm`: to unban a banned user\n
          /deleteUser `id/usrnm`: delete user from database\n
          /forward `id/usrnm`: replied message forward to user\n
          /forward c `id/usrnm`: replied message forward as copy\n
          /users: get current bot users list\n
          /broadcast: replied message broadcast to all users\n
          /broadcast f: replied message forward to bot users"""
footer="""\n\nSource-Code: [i💜PDF](https://github.com/nabilanavab/iLovePDF)\n
       Bot: @complete_pdf_bot 💎\n
       [Support Channel](https://telegram.dog/iLovePDF_bot)"""


# ❌ CANCELS CURRENT PDF TO IMAGES WORK ❌
@ILovePDF.on_message(filters.private & filters.command(["cancel"]) & filters.incoming)
async def cancelP2I(bot, message):
    try:
        PROCESS.remove(message.chat.id)
        await message.delete()          # delete /cancel if process canceled
    except Exception:
        try:
            await message.reply_chat_action("typing")
            await message.reply_text(
                                    '🤔', quote=True
                                    )
        except Exception:
            pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message(filters.private & filters.command(["delete"]) & filters.incoming)
async def _cancelI2P(bot, message):
    try:
        await message.reply_chat_action("typing")
        del PDF[message.chat.id]
        await message.reply_text(
                                "`Queue deleted Successfully..`🤧",
                                quote=True
                                )
        shutil.rmtree(f"{message.chat.id}")
    except Exception:
        await message.reply_text(
                                "`No Queue founded..`😲",
                                quote=True
                                )

# ❌ GET USER ID (/id) ❌
@ILovePDF.on_message(filters.private & filters.command(["id"]) & filters.incoming)
async def userId(bot, message):
    try:
        userINFO=await message.get_users()
        # userINFO=await bot.get_users(message.chat.id)
        await message.reply_text(
                                f'{userINFO.mention} Id: `{message.chat.id}`',
                                quote=True
                                )
    except Exception:
        pass

# ❌ GET FEEDBACK MESSAGE ❌
@ILovePDF.on_message(filters.private & filters.command(["feedback"]) & filters.incoming)
async def feedback(bot, message):
    try:
        await message.reply_text(
                                feedbackMsg,
                                disable_web_page_preview=True
                                )
    except Exception:
        pass

# ❌ DELETS CURRENT IMAGES TO PDF QUEUE (/delete) ❌
@ILovePDF.on_message(filters.private & filters.command(["help", "commands"]) & filters.incoming)
async def _help(bot, message):
    try:
        await message.reply_chat_action("typing")
        helpMsg=await message.reply(
                                   "⚙️ Processing..", quote=True
                                   )
        await sleep(1)
        HELP=userHELP
        await helpMsg.edit(HELP)
        if message.chat.id in ADMIN:
            HELP=userHELP+adminHelp
            await helpMsg.edit(Help)
        await sleep(1)
        HELP+=footer
        await helpMsg.edit(HELP)
    except Exception:
        pass
#                                                                                  Telegram: @nabilanavab
