# fileName : plugins/dm/server.py
# copyright ©️ 2021 nabilanavab

import shutil
from database import db
from pyrogram import filters
from Configs.dm import Config
from Configs.db import dataBASE
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF

@ILovePDF.on_message(filters.private & filters.command(["server"]) & ~filters.edited & filters.user(Config.ADMINS))
async def server(bot, message):
    try:
        total, used, free = shutil.disk_usage(".")
        total=await gSF(total)
        used=await gSF(used)
        free=await gSF(free)
        if dataBASE.MONGODB_URI:
            total_users=await db.total_users_count()
        else:
            total_users="Not Counted yet.. 🥱"
        await message.reply_text(
            text=f"**Total Disk Space:** {total} \n"
                 f"**Free Space:** {free} \n"
                 f"**Total Users in DB:** `{total_users}`",
            quote=True
        )
    except Exception as e:
        print("plugin/dm/server: ", e)

#                                                                             Telegram: @nabilanavab
