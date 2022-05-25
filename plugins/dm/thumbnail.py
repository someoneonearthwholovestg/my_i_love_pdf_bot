# fileName : plugins/dm/thumbnail.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import asyncio
from pyromod import listen
from pyrogram import filters
from plugins.dm.start import _back
from configs.db import isMONGOexist
from pyrogram import Client as ILovePDF
from pyrogram.types import InputMediaPhoto
from configs.images import PDF_THUMBNAIL, WELCOME_PIC
from configs.images import CUSTOM_THUMBNAIL_U, CUSTOM_THUMBNAIL_C
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if isMONGOexist:
    from database import db

# NB: lots and lots and lots of time wasted.. 😓
# https://docs.pyrogram.org/api/methods/edit_message_media

# CUSTOM THUMBNAIL 
@ILovePDF.on_message(
                    ~filters.edited
                    filters.command("thumbnail") &
                    (filters.private | filters.group)
                    )
async def _thumbnail(bot, message):
    try:
        chat_type = message.chat.type
        if not isMONGOexist:
            # if No mongoDB Url
            await message.reply(
                               "Can't Use This Feature 🤧",
                               quote = True
                               )
            return
        elif message.reply_to_message and message.reply_to_message.photo:
            # set thumbnail
            if chat_type == "private":
                await db.set_thumbnail(
                                      message.chat.id,
                                      message.reply_to_message.photo.file_id
                                      )
            else:
                await db.set_chat_thum(
                                      message.chat.id,
                                      message.reply_to_message.photo.file_id
                                      )
            await message.reply_photo(
                                     photo = message.reply_to_message.photo.file_id,
                                     caption = "Okay,\n"
                                              "I will use this image as custom thumbnail.. 🖐️",
                                     reply_markup = InlineKeyboardMarkup(
                                              [[InlineKeyboardButton("Delete Thumbnail",
                                                       callback_data = "delThumb")]]
                                     ),
                                     quote = True
                                     )
            if chat_type = "private":
                CUSTOM_THUMBNAIL_U.append(message.from_user.id)
            else:
                CUSTOM_THUMBNAIL_C.append(message.chat.id)
            return
        else:
            if (chat_type == "private") and (message.chat.id not in CUSTOM_THUMBNAIL_U):
                return await message.reply(
                                    "You didn't set custom thumbnail!\n"
                                    "reply /thumbnail to set thumbnail",
                                    quote = True
                                    )
            # non private messages ↓
            if message.chat.id in CUSTOM_THUMBNAIL_C:
                return await message.reply(
                                    "No Custom Group Thumbnail 🥲",
                                    quote = True
                                    )
            # Get Thumbnail from DB
            if chat_type == "private":
                thumbnail = await db.get_thumbnail(message.from_user.id)
            else:
                thumbnail = await db.get_chat_thumb(message.chat.id)
            await message.reply_photo(
                                     photo = thumbnail,
                                     caption = "Custom Thumbnail",
                                     quote = True,
                                     reply_markup = InlineKeyboardMarkup(
                                            [[InlineKeyboardButton("Delete Thumbnail",
                                                   callback_data = "delThumb")]]
                                     ))
            return
    except Exception as e:
        logger.exception(
                        "/THUMBNAIL:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


geThumb = filters.create(lambda _, __, query: query.data=="getThumb")
addThumb = filters.create(lambda _, __, query: query.data=="addThumb")
delThumb = filters.create(lambda _, __, query: query.data=="delThumb")


@ILovePDF.on_callback_query(geThumb)
async def _getThumb(bot, callbackQuery):
    try:
        chat_type = callbackQuery.chat.type
        if not isMONGOexist:
            await callbackQuery.answer(
                                      "Can't Use This Feature 🤧"
                                      )
            return
        else:
            await callbackQuery.answer(
                                      "wait.! Let me think.. 🤔"
                                      )
            
            if callbackQuery.chat.id in CUSTOM_THUMBNAIL_U:
                thumbnail = await db.get_thumbnail(
                                                  callbackQuery.chat.id
                                                  )
            elif callbackQuery.chat.id in CUSTOM_THUMBNAIL_C:
                thumbnail = await db.get_chat_thumb(
                                                   callbackQuery.chat.id
                                                   )
            else:
                thumbnail = False
            
            if not thumbnail:
                await callbackQuery.edit_message_media(InputMediaPhoto(PDF_THUMBNAIL))
                if chat_type == "private":
                    reply_markup = InlineKeyboardMarkup(
                                        [[InlineKeyboardButton("😒 ADD THUMB 😒",
                                                       callback_data = "addThumb")],
                                         [InlineKeyboardButton("« BACK «",
                                                          callback_data = "back")]]
                                   )
                else:
                    reply_markup = InlineKeyboardMarkup(
                                        [[InlineKeyboardButton("« BACK «",
                                                          callback_data = "back")]]
                                   )
                await callbackQuery.edit_message_caption(
                                                        caption = "🌟 CURRENT THUMBNAIL 🌟 (DEFAULT)\n\n"
                                                                  "You didn't set any custom thumbnail!\n\n"
                                                                  "/thumbnail :\n◍ To get current thumbnail\n"
                                                                  "◍ Reply to a photo to set custom thumbnail",
                                                        reply_markup = reply_markup
                                                        )
                return
            await callbackQuery.edit_message_media(InputMediaPhoto(thumbnail))
            if chat_type == "private":
                reply_markup = InlineKeyboardMarkup(
                                     [[InlineKeyboardButton("🥲 CHANGE 🥲",
                                                callback_data = "addThumb"),
                                       InlineKeyboardButton("🤩 DELETE 🤩",
                                                callback_data = "delThumb")],
                                      [InlineKeyboardButton("« BACK «",
                                                callback_data = "back")]]
                               )
            else:
                reply_markup = InlineKeyboardMarkup(
                                     [[InlineKeyboardButton("« BACK «",
                                                callback_data = "back")]]
                               )
            await callbackQuery.edit_message_caption(
                                                    caption = "🌟 CURRENT THUMBNAIL 🌟\n\n"
                                                              "/thumbnail :\n◍ To get current thumbnail\n"
                                                              "◍ Reply to a photo to set custom thumbnail",
                                                    reply_markup = reply_markup)
            return
    except Exception as e:
        logger.exception(
                        "GET_THUMB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(addThumb)
async def _addThumb(bot, callbackQuery):
    try:
        await callbackQuery.answer()
        await callbackQuery.edit_message_caption(
                                                caption = "Now, Send me a Image..",
                                                reply_markup = InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("Waiting.. 🥱",
                                                             callback_data = "noResponse")]]
                                                ))
        await asyncio.sleep(1)
        await callbackQuery.edit_message_caption(
                                                caption = "Now, Send me a Image for Future Use.. 😅\n\n"
                                                          "Don't have enough time, send me fast 😏",
                                                reply_markup = InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("Waiting.. 🥱",
                                                             callback_data = "noResponse")]]
                                                ))
        getThumb = await bot.listen(
                                   callbackQuery.from_user.id
                                   )
        if not getThumb.photo:
            await getThumb.delete()
            await _back(bot, callbackQuery)
        else:
            await callbackQuery.edit_message_media(InputMediaPhoto(getThumb.photo.file_id))
            await callbackQuery.edit_message_caption(
                                                    caption = "🌟 CURRENT THUMBNAIL 🌟\n\n"
                                                              "/thumbnail :\n◍ To get current thumbnail\n"
                                                              "◍ Reply to a photo to set custom thumbnail",
                                                    reply_markup = InlineKeyboardMarkup(
                                                        [[InlineKeyboardButton("🥲 CHANGE 🥲",
                                                                       callback_data = "addThumb"),
                                                          InlineKeyboardButton("🤩 DELETE 🤩",
                                                                      callback_data = "delThumb")],
                                                         [InlineKeyboardButton("« BACK «",
                                                                          callback_data = "back")]]
                                                    ))
            await db.set_thumbnail(
                                  callbackQuery.from_user.id,
                                  getThumb.photo.file_id
                                  )
            await getThumb.delete()
            CUSTOM_THUMBNAIL_U.append(
                                     callbackQuery.message.chat.id
                                     )
    except Exception as e:
        logger.exception(
                        "ADD_THUMB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

@ILovePDF.on_callback_query(delThumb)
async def _delThumb(bot, callbackQuery):
    try:
        chat_type = callbackQuery.chat.type
        # if callbackQuery for [old delete thumb] messages
        if callbackQuery.chat.id not in CUSTOM_THUMBNAIL_U or CUSTOM_THUMBNAIL_C:
            return await callbackQuery.answer(
                                             "Currently, you don't set a thumbnail yet.. 🤧"
                                             )
        await callbackQuery.answer(
                                  "Deleted.. 😎"
                                  )
        await callbackQuery.edit_message_media(InputMediaPhoto(WELCOME_PIC))
        await _back(bot, callbackQuery)
        
        if chat_type = "private":
            await db.set_thumbnail(
                                  callbackQuery.chat.id,
                                  None
                                  )
            CUSTOM_THUMBNAIL_U.remove(
                                     callbackQuery.chat.id
                                     )
        else:
            await db.set_chat_thum(
                                  callbackQuery.chat.id,
                                  None
                                  )
            CUSTOM_THUMBNAIL_C.remove(
                                     callbackQuery.chat.id
                                     )
    except Exception as e:
        logger.exception(
                        "DEL_THUMB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

#                                                                                              Telegram: @nabilanavab
