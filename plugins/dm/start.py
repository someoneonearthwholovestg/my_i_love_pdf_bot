# fileName : plugins/dm/start.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

from pdf import invite_link
from pyrogram import filters
from configs.dm import Config
from plugins.dm.photo import images
from pyrogram import Client as ILovePDF
from plugins.dm.document import documents
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardMarkup
from configs.db import isMONGOexist, LOG_CHANNEL
from configs.images import WELCOME_PIC, BANNED_PIC

if isMONGOexist:
    from database import db

#------------------->
#--------> LOCAL VARIABLES
#------------------->

welcomeMsg = """Hey [{}](tg://user?id={})..!!
This bot will helps you to do many things with pdf's 🥳

Some of the main features are:
◍ `Convert images to PDF`
◍ `Convert PDF to images`
◍ `Convert files to pdf`"""

forceSubMsg = """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only Channel Members Can Use this Bot 🚶

This Means You Need To Join The Below Mentioned Channel for Using Me!

Hit on `"♻️retry♻️"` after joining.. 😅"""

helpMessage = """Hey  [{}](tg://user?id={}).! this is a HELP MESSAGE:

This Bot will Helps you to do many things with pdfs
Some of the main features are:

Owned By: @nabilanavab

- Convert Different Codecs to PDF
    ~.epub, ... [unlimited]
    ~45 Other Codecs by API TOkEN
- PDF Manipulation:
    ~ Fetch metaData
    ~ Merge multiple PDF's
    ~ Split PDF's to parts
    ~ PDF to Images
    ~ PDF to text, html,
    ~ PDF to message, json
    ~ Zip / Rar PDF pages
    ~ Encrypt PDF
    ~ Decrypt PDF
"""

foolRefresh = "വിളച്ചിലെടുക്കല്ലേ കേട്ടോ 😐"

LOG_TEXT = "#newUser @nabilanavab/ILovePDF\nID: {}\nView Profile: {}"

button = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🌍 SET LANG 🌍", callback_data="underDev")
        ],[
            InlineKeyboardButton("📌 SET THUMB 📌", callback_data="getThumb"),
            InlineKeyboardButton("💩 SET API 💩", callback_data="underDev")
        ],[
            InlineKeyboardButton("🔎 ABOUT & HELP 🔎", callback_data="help")
        ],[
            InlineKeyboardButton("🌟 SOURCE CODE 🌟", url="https://github.com/nabilanavab/ilovepdf")
        ],[
            InlineKeyboardButton("🤖 CHANNEL 🤖", url="https://telegram.dog/ilovepdf_bot"),
            InlineKeyboardButton("📝 FEEDBACK 📝", url="https://t.me/ilovepdf_bot/14?comment=10000")
        ],[
            InlineKeyboardButton("➕ ADD TO GROUP ➕", callback_data="underDev")
        ],[
            InlineKeyboardButton("† CLOSE †", callback_data="close")
        ]]
    )

UPDATE_CHANNEL = Config.UPDATE_CHANNEL

#--------------->
#--------> /start (START MESSAGE)
#------------------->

@ILovePDF.on_message(filters.private & ~filters.edited & filters.command(["start", "ping"]) & filters.incoming)
async def start(bot, message):
    try:
        global invite_link
        await message.reply_chat_action(
                                       "typing"
                                       )
        # CHECK IF USER IN DATABASE
        if isMONGOexist:
            if not await db.is_user_exist(message.from_user.id):
                await db.add_user(
                                 message.from_user.id,
                                 message.from_user.first_name
                                 )
                if LOG_CHANNEL:
                    await bot.send_message(
                                          chat_id = LOG_CHANNEL,
                                          text = LOG_TEXT.format(message.from_user.id, message.from_user.mention),
                                          reply_markup = InlineKeyboardMarkup(
                                                      [[InlineKeyboardButton("« B@N «", callback_data=f"banU|{chat_id}")]]
                                          ))
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus = await bot.get_chat_member(
                           str(UPDATE_CHANNEL), message.chat.id
                           )
                # IF USER BANNED FROM CHANNEL
                if userStatus.status == 'banned':
                     await message.reply_photo(
                                              photo = BANNED_PIC,
                                              caption = "For Some Reason You Can't Use This Bot"
                                                       "\n\nContact Bot Owner 🤐",
                                              reply_markup = InlineKeyboardMarkup(
                                                             [[InlineKeyboardButton("Owner 🎊", url = "https://t.me/nabilanavab")]]
                                              ))
                     return
            except Exception as e:
                if invite_link==None:
                    invite_link=await bot.create_chat_invite_link(int(UPDATE_CHANNEL))
                await message.reply_photo(
                                         photo = WELCOME_PIC,
                                         caption = forceSubMsg.format(
                                                                   message.from_user.first_name,
                                                                   message.chat.id
                                                                   ),
                                         reply_markup = InlineKeyboardMarkup(
                                              [[
                                                      InlineKeyboardButton("🌟 JOIN CHANNEL 🌟",
                                                                    url = invite_link.invite_link)
                                              ],[
                                                      InlineKeyboardButton("♻️ REFRESH ♻️",
                                                                    callback_data = "refresh")
                                              ]]
                                         ))
                await message.delete()
                return
        # IF NO FORCE SUBSCRIPTION
        await message.reply_photo(
                                 photo = WELCOME_PIC,
                                 caption = welcomeMsg.format(
                                                          message.from_user.first_name,
                                                          message.chat.id
                                 ),
                                 reply_markup = button
                                 )
        # DELETES /start MESSAGE
        await message.delete()
    except Exception as e:
        logger.exception(
                        "PHOTO:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


#--------------->
#--------> START CALLBACKS
#------------------->

refreshDoc = filters.create(lambda _, __, query: query.data == "refreshDoc")
refreshImg = filters.create(lambda _, __, query: query.data == "refreshImg")
refresh = filters.create(lambda _, __, query: query.data == "refresh")
close = filters.create(lambda _, __, query: query.data == "close")
back = filters.create(lambda _, __, query: query.data == "back")
hlp = filters.create(lambda _, __, query: query.data == "help")

@ILovePDF.on_callback_query(hlp)
async def _hlp(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_caption(
              caption = helpMessage.format(
                        callbackQuery.from_user.first_name, callbackQuery.message.chat.id
                        ),
                        reply_markup = InlineKeyboardMarkup(
                              [[InlineKeyboardButton("« BACK «",
                                       callback_data = "back")]]
              ))
    except Exception as e:
        logger.exception(
                        "HLP:CAUSES %(e)s ERROR",
                        exc_info = True
                        )


@ILovePDF.on_callback_query(back)
async def _back(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_caption(
              caption = welcomeMsg.format(
                        callbackQuery.from_user.first_name,
                        callbackQuery.message.chat.id
              ),
              reply_markup = button
              )
    except Exception as e:
        logger.exception(
                        "BACK:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


@ILovePDF.on_callback_query(refresh | refreshDoc | refreshImg)
async def _refresh(bot, callbackQuery):
    try:
        # CHECK USER IN CHANNEL (REFRESH CALLBACK)
        userStatus = await bot.get_chat_member(
                                              str(UPDATE_CHANNEL),
                                              callbackQuery.message.chat.id
                                              )
        # IF USER NOT MEMBER (ERROR FROM TG, EXECUTE EXCEPTION)
        if callbackQuery.data == "refresh":
            return await callbackQuery.edit_message_caption(
                          caption = welcomeMsg.format(
                                      callbackQuery.from_user.first_name,
                                      callbackQuery.message.chat.id
                                      ),
                                      reply_markup = button
                         )
        if callbackQuery.data == "refreshDoc":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return documents(
                            bot, messageId
                            )
        if callbackQuery.data == "refreshImg":
            messageId = callbackQuery.message.reply_to_message
            await callbackQuery.message.delete()
            return images(
                         bot, messageId
                         )
    except Exception as e:
        logger.exception(
                        "REFRESH:CAUSES %(e)s ERROR",
                        exc_info=True
                        )
        try:
            # IF NOT USER ALERT MESSAGE (AFTER CALLBACK)
            await bot.answer_callback_query(
                                           callbackQuery.id,
                                           text = foolRefresh,
                                           show_alert = True,
                                           cache_time = 0
                                           )
        except Exception:
            pass

@ILovePDF.on_callback_query(close)
async def _close(bot, callbackQuery):
    try:
        await callbackQuery.message.delete()
    except Exception as e:
        logger.exception(
                        "CLOSE:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


#                                                                                  Telegram: @nabilanavab
