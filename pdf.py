# This file is part of nabilanavab/iLovePDF [a completely free software]


# Repository:  : [i💜PDF]
# Author:      : nabilanavab
# Email:       : nabilanavab@gmail.com
# Telegram:    : https://telegram.dog/complete_pdf_bot
# GitHub:      : https://github.com/nabilanavab/ILovePDF
# Coding       : !/usr/bin/python3, utf-8, copyright ©️ 2021 nabilanavab


# ABOUT SOURCE-CODE:
#     Inspired from an old Telegram Bot [@JPG2PDFBot] by @spechide
# 
# When I released nabilanavab/ILovePDF in 2021-JUNE, It had Only 100 lines of code.
# at that time, bot only supports images to PDF feature, Having worked on it for
# a few more weeks, it made me more interesting In adding new features. Now, it
# supports many manipulation over TELEGRAM PDF files..
#                                       THANKS ALL MY COLLEGE'S FOR SUGGESTIONS 💚
# 
# Before blaming the source-code:
#    ◍ I'm neither a Geek nor a Computer Science student
#    ◍ Just Started Writing this Source-code when I was 19 :)
#    ◍ Source-code was fully written using my Android phone [Nokia 2.2]
#                      funFact: I never had hosted this program locally yet :(
#
#                                                     CURRENTLY A [BSC. PHYSICS STUDENT]
#                                                          DATE:[1-JUNE-2022, Wednesday]


'''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         [Nabil A Navab] 
                         Email: nabilanavab@gmail.com
                         Telegram: @nabilanavab
'''


import logging
from pyromod import listen
from configs.dm import Config
from configs.db import isMONGOexist
from pyrogram import Client as ILovePDF
from configs.db import BANNED_USR_DB, BANNED_GRP_DB
from configs.images import CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if isMONGOexist:
    from database import db


# LOGGING INFO: DEBUG
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )
logging.getLogger("pyrogram").setLevel(logging.ERROR)
# SOMEONE TOLD ME HONEY DEV. NEVER USE PRINT FOR TRACKING ERRORS. SO, import logging :|


# GLOBAL VARIABLES
PDF={}            # save images for generating pdf
PROCESS=[]        # to check current process
invite_link=None


class Bot(ILovePDF):
    
    def __init__(self):
        super().__init__(
            session_name="ILovePDF",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.API_TOKEN,
            plugins={"root": "plugins"},
        )
    
    async def start(self):
        
        if isMONGOexist:
            
            logger.debug("Loading users from DataBase..")
            # Loading Banned UsersId to List
            b_users, b_chats = await db.get_banned()
            BANNED_USR_DB.extend(b_users)
            BANNED_GRP_DB.extend(b_chats)
            
            logger.debug("Loading Users having custom thumb..")
            # Loading UsersId with custom THUMBNAIL
            users = await db.get_all_users()   # Get all user Data
            for user in users:
                if user.get("thumbnail", False):
                    CUSTOM_THUMBNAIL_U.append(user["id"])
            groups = await db.get_all_chats()
            for group in groups:
                if group.get("thumbnail", False):
                    CUSTOM_THUMBNAIL_C.append(group["id"])
            
            # Bot Restarted Message to ADMINS
            for admin in Config.ADMINS:
                try:
                    await Bot.send_message(
                                          chat_id=admin,
                                          text="Bot Started Working.. 😳",
                                          reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton("◍ close ◍",
                                                        callback_data="close")]]
                                          ))
                except Exception:
                    logger.debug(
                                 "{} not started Bot yet :(".format(admin)
                                 )
            
            logger(f"Bot Started..")
            await super().start()
    
    async def stop(self, *args):
        await super().stop()


if __name__ == "__main__":
    app=Bot()
    app.run()

#                                                         OPEN SOURCE TELEGRAM PDF BOT 🐍
#                                                              by: nabilanavab [iLovePDF]
