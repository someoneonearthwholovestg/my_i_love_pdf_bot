# fileName : plugins/dm/admin.py
# copyright ©️ 2021 nabilanavab

import shutil
import psutil
from pdf import PROCESS
from pyrogram import filters
from configs.dm import Config
from configs.db import dataBASE
from pyrogram.types import Message
from configs.db import isMONGOexist
from configs.group import groupConfig
from configs.images import BANNED_PIC
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from plugins.fileSize import get_size_format as gSF

BANNED_USR_DB, BANNED_GRP_DB=[], []

if isMONGOexist:
    from database import db
    
    async def banUsr():
        userBANNED_db, groupBANNED_db=await db.get_banned()
        BANNED_USR_DB=userBANNED_db
        BANNED_GRP_DB=groupBANNED_db

#--------------->
#--------> config vars
#------------------->

BANNED_GROUP=groupConfig.BANNED_GROUP
ONLY_GROUP=groupConfig.ONLY_GROUP
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

UCantUse="Hey {}\nFOR SOME REASON YOU CANT USE THIS BOT :("

GroupCantUse="{} NEVER EXPECT A GOOD RESPONSE FROM ME\n\nADMINS RESTRICTED ME FROM WORKING HERE.. 🤭"

button=InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Create your Own Bot", url="https://github.com/nabilanavab/ilovepdf")
        ],[
            InlineKeyboardButton("Tutorial", url="t.me/ilovepdf_bot")
        ],[
            InlineKeyboardButton("Update Channel", url="t.me/ilovepdf_bot")
        ]]
    )

#--------------->
#--------> LOCAL FUNCTIONs
#------------------->

async def bannedUsers(_, __, message: Message):
    if isMONGOexist:
        await banUsr()
    if (message.from_user.id in BANNED_USERS) or (
               (ADMIN_ONLY) and (message.from_user.id not in ADMINS)) or (
               (BANNED_USR_DB) and (message.from_user.id in BANNED_USR_DB)):
        return True
    return False

banned_user=filters.create(bannedUsers)

async def bannedGroups(_, __, message: Message):
    if (message.chat.id in BANNED_GROUP) or (
               (ONLY_GROUP) and (message.chat.id not in ONLY_GROUP)) or (
               (BANNED_GRP_DB) and (message.chat.id in BANNED_GRP_DB)):
        return True
    return False

banned_group=filters.create(bannedGroups)

@ILovePDF.on_message(filters.private & banned_user & filters.incoming)
async def bannedUsr(bot, message):
    try:
        await message.reply_chat_action("typing")
        # IF USER BANNED FROM DATABASE
        if message.from_user.id in BANNED_USR_DB:
            ban=await db.get_ban_status(message.from_user.id)
            await message.reply_photo(
                                photo=BANNED_PIC,
                                caption=UCantUse.format(message.from_user.mention)+f'\n\nREASON: {ban["ban_reason"]}',
                                reply_markup=button, quote=True
                                )
            return
        #IF USER BANNED FROM CONFIG.VAR
        await message.reply_photo(
                            photo=BANNED_PIC,
                            caption=UCantUse.format(message.from_user.mention),
                            reply_markup=button, quote=True
                            )
    except Exception:
        pass

@ILovePDF.on_message(filters.group & banned_group & filters.incoming)
async def bannedGrp(bot, message):
    try:
        await message.reply_chat_action("typing")
        if message.chat.id in BANNED_GRP_DB:
            ban=await db.get_ban_status(message.chat.id)
            toPin=await message.reply_photo(
                                      photo=BANNED_PIC,
                                      caption=GroupCantUse.format(message.chat.mention)+f'\n\nREASON: {ban["ban_reason"]}',
                                      reply_markup=button, quote=True
                                      )
        else:
            toPin=await message.reply_photo(
                                      photo=BANNED_PIC,
                                      caption=GroupCantUse.format(message.chat.mention),
                                      reply_markup=button, quote=True
                                      )
        try:
            await toPin.pin()
        except Exception:
            pass
        await bot.leave_chat(message.chat.id)
    except Exception:
        pass


# ❌ ADMIN COMMAND (/server) ❌
@ILovePDF.on_message(filters.private & filters.command(["server"]) & filters.incoming & filters.user(Config.ADMINS))
async def server(bot, message):
    try:
        try:
            await await banUsr()
            await message.reply(BANNED_USR_DB)
        except Exception as e:
            await message.reply(e)
        total, used, free = shutil.disk_usage(".")
        total=await gSF(total);used=await gSF(used); free=await gSF(free)
        cpu_usage=psutil.cpu_percent()
        ram_usage=psutil.virtual_memory().percent
        disk_usage=psutil.disk_usage('/').percent
        if isMONGOexist:
            total_users=await db.total_users_count()
            total_chats=await db.total_chat_count()
        else:
            total_users="No DB"; total_chats="No DB"
        await message.reply_text(
                            text=f"**◍ Total Space     :** `{total}` \n"
                                 f"**◍ Used Space     :** `{used}({disk_usage}%)` \n"
                                 f"**◍ Free Space      :** `{free}` \n"
                                 f"**◍ CPU Usage      :** `{cpu_usage}`% \n"
                                 f"**◍ RAM Usage     :** `{ram_usage}`%\n"
                                 f"**◍ Current Work  :** `{len(PROCESS)}`\n"
                                 f"**◍ DB Users         :** `{total_users}`\n"
                                 f"**◍ DB Grups         :** `{total_chats}`\n"
                                 f"**◍ Message Id     :** `{message.message_id}`",
                            reply_markup=InlineKeyboardMarkup(
                                 [[
                                     InlineKeyboardButton("⟨ CLOSE ⟩",
                                            callback_data="closeALL")
                                 ]]
                                 ),
                            quote=True
                            )
    except Exception as e:
        print("plugin/dm/server: ", e)

#                                                                                                        Telegram: @nabilanavab
