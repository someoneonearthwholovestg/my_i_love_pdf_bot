# fileName : plugins/dm/waste.py
# copyright ©️ 2021 nabilanavab

from pyrogram import filters
from configs.dm import Config
from pyrogram import Client as ILovePDF


#--------------->
#--------> PDF REPLY BUTTON
#------------------->

@ILovePDF.on_message(
                    filters.private &
                    ~filters.edited &
                    filters.incoming &
                    ~filters.user(Config.ADMINS)
                    )
async def _spam(bot, message):
    try:
        await message.reply_chat_action(
                                       "typing"
                                       )
        await message.reply_text(
                                f"`no one gonna to help you` 😏",
                                quote=True
                                )
    except Exception:
        pass

#                                                     Telegram: @nabilanavab
