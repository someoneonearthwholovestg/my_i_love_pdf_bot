# !/USR/BIN/PYTHON
# -*- COADING: UTF-8 -*-
# COPYRIGHT ©️ 2021 NABILANAVAB

'''
  _   _                  ___  ___  ____ ™
 | | | |   _____ _____  | _ \|   \|  __| 
 | | | |__/ _ \ V / -_) |  _/| |) |  _|  
 |_| |___,\___/\_/\___| |_|  |___/|_|    
                         [Nabil A Navab] 
                         Email: nabilanavab@gmail.com
                         Telegram: @nabilanavab
 '''
import asyncio
import logging
from pyromod import listen
from configs.dm import Config
#from pyrogram import Client, idle
from pyrogram import Client as ILovePDF
from configs.db import isMONGOexist
from configs.db import BANNED_USR_DB, BANNED_GRP_DB

if isMONGOexist:
    from database import db

# LOGGING INFO: DEBUG
logging.basicConfig(
    level = logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# GLOBAL VARIABLES
PDF={}            # save images for generating pdf
PROCESS=[]        # to check current process
invite_link=None


# PLUGIN DIRECTORY
plugin=dict(root="plugins")

"""
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
            b_users, b_chats = await db.get_banned()
            BANNED_USR_DB=b_users
            BANNED_GRP_DB=b_chats
            await super().start()
    
    async def stop(self, *args):
        await super().stop()

app=Bot()
app.run()

"""
# PYROGRAM BOT AUTHENTIFICATION
bot=Client(
    "ILovePDF",
    plugins=plugin,
    api_id=Config.API_ID,
    parse_mode="markdown",
    api_hash=Config.API_HASH,
    bot_token=Config.API_TOKEN
)


bot.start()
idle()
bot.stop()

