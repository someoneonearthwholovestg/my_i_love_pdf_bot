# fileName : plugins/adminCheck.py
# copyright ©️ 2021 nabilanavab


# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

from configs.dm import Config
from configs.group import groupConfig

ONLY_GROUP_ADMIN = groupConfig.ONLY_GROUP_ADMIN


async def adminCheck(message):
    try:
        if (ONLY_GROUP_ADMIN) or (message.from_user.id != message.reply_to_message.from_user.id):
            if message.from_user.id in config.ADMINS:
                pass
            else:
                userStat = bot.get_chat_member(
                                              message.chat.id,
                                              message.from_user.id
                                              )
                if userStat.status not in ["administrator", "owner"]:
                    await message.reply(
                                       "`Either you must be an admin or you need to reply to your own message` 😅"
                                       )
                    return False
        return True
    except Exception as e:
        logger.exception(
                        "»»adminCheck:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


async def adminCheckCB(callbackQuery):
    try:
        if (ONLY_GROUP_ADMIN) or (callbackQuery.from_user.id != callbackQuery.message.reply_to_message.from_user.id):
            if callbackQuery.from_user.id in config.ADMINS:
                pass
            else:
                userStat = bot.get_chat_member(
                                              callbackQuery.message.chat.id,
                                              callbackQuery.from_user.id
                                              )
                if userStat.status not in ["administrator", "owner"]:
                    await message.reply(
                                       "`Either you must be an admin or you need to reply to your own message` 😅"
                                       )
                    return False
        return True
    except Exception as e:
        logger.exception(
                        "»»adminCheckCB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
