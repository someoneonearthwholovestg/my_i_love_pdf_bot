# fileName : plugins/dm/banned.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from Configs.dm import Config
from Configs.group import groupConfig
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from Configs.db import BANNED_USR_DB, BANNED_GRP_DB

#--------------->
#--------> config vars
#------------------->

BANNED_GROUP=groupConfig.BANNED_GROUP
ONLY_GROUP=groupConfig.ONLY_GROUP
BANNED_USERS=Config.BANNED_USERS
ADMIN_ONLY=Config.ADMIN_ONLY
ADMINS=Config.ADMINS

PIC="./IMAGES/banned.jpeg"

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
    if (message.from_user.id in BANNED_USERS) or
        ((ADMIN_ONLY) and (message.from_user.id not in ADMINS)) or
        ((BANNED_USR_DB) and (message.from_user.id not in BANNED_USR_DB)):
        return True
    return False

banned_user=filters.create(bannedUsers)

async def bannedGroups(_, __, message: Message):
    if (message.chat.id in BANNED_GROUP) or
        ((ONLY_GROUP) and (message.chat.id not in ONLY_GROUP)) or
        ((BANNED_GRP_DB) and (message.chat.id not in BANNED_GRP_DB)):
        return True
    return False

banned_group=filters.create(bannedGroups)

@ILovePDF.on_message(filters.private & banned_user)
async def bannedUsr(bot, message):
    try:
        await message.reply_chat_action("typing")
        # IF USER BANNED FROM DATABASE
        if message.from_user.id in BANNED_USR_DB:
            ban=await db.get_ban_status(message.from_user.id)
            await message.reply_photo(
                photo=PIC, caption=UCantUse.format(message.from_user.mention)+f"\n\nREASON: {ban["ban_reason"]}",
                reply_markup=button, quote=True
            )
            return
        #IF USER BANNED FROM CONFIG.VAR
        await message.reply_photo(
            photo=PIC, caption=UCantUse.format(message.from_user.mention),
            reply_markup=button, quote=True
        )
    except Exception:
        pass

@ILovePDF.on_message(filters.group & banned_group)
async def bannedGrp(bot, message):
    try:
        await message.reply_chat_action("typing")
        if message.chat.id in BANNED_GRP_DB:
            ban=await db.get_ban_status(message.chat.id)
            toPin=await message.reply_photo(
                photo=PIC, caption=GroupCantUse.format(message.chat.mention)+f"\n\nREASON: {ban["ban_reason"]}",
                reply_markup=button, quote=True
            )
        else:
            toPin=await message.reply_photo(
                photo=PIC, caption=GroupCantUse.format(message.chat.mention),
                reply_markup=button, quote=True
            )
        try:
            await toPin.pin()
        except Exception:
            pass
        await bot.leave_chat(message.chat.id)
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
