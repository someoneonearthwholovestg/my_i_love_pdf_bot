# fileName : plugins/dm/server.py
# copyright ©️ 2021 nabilanavab

import shutil
import psutil
from pdf import PROCESS
from pyrogram import filters
from Configs.dm import Config
from Configs.db import isMONGOexist
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if isMONGOexist:
    from database import db


@ILovePDF.on_message(filters.private & filters.command(["server"]) & ~filters.edited & filters.user(Config.ADMINS))
async def server(bot, message):
    try:
        total, used, free = shutil.disk_usage(".")
        total=await gSF(total)
        used=await gSF(used)
        free=await gSF(free)
        cpu_usage=psutil.cpu_percent()
        ram_usage=psutil.virtual_memory().percent
        disk_usage=psutil.disk_usage('/').percent
        if isMONGOexist:
            total_users=await db.total_users_count()
        else:
            total_users="No DB"
        await message.reply_text(
            text=f"**◍ Total Space   :** `{total}` \n"
                 f"**◍ Used Space   :** `{used}({disk_usage}%)` \n"
                 f"**◍ Free Space    :** `{free}` \n"
                 f"**◍ CPU Usage    :** `{cpu_usage}`% \n"
                 f"**◍ RAM Usage   :** `{ram_usage}`%\n"
                 f"**◍ Current Work :** `{len(PROCESS)}`\n"
                 f"**◍ DB Users       :** `{total_users}`"
                 f"**◍ Message Id     :** `{message.message_id}`",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("⟨ CLOSE ⟩", callback_data="closeALL")
                ]]
            ),
            quote=True
        )
    except Exception as e:
        print("plugin/dm/server: ", e)

#                                                                             Telegram: @nabilanavab
