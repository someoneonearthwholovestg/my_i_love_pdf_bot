# fileName : plugins/dm/thumbnail.py
# copyright ©️ 2021 nabilanavab

from plugins.dm.start import _back
from pyromod import listen
from pyrogram import filters
from configs.db import isMONGOexist
from pyrogram import Client as ILovePDF
from configs.images import PDF_THUMBNAIL, WELCOME_PIC
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

if isMONGOexist:
    from database import db

# CUSTOM THUMBNAIL 
@ILovePDF.on_message(
                    filters.command("thumbnail") &
                    filters.private & ~filters.edited
                    )
async def _thumbnail(bot, message):
    try:
        if not isMONGOexist:
            # if No mongoDB Url
            await message.reply(
                               "Can't Use This Feature 🤧",
                               quote=True
                               )
            return
        elif message.reply_to_message.photo:
            # set thumbnail
            await db.set_thumbnail(
                message.from_user.id, message.reply_to_message.photo.file_id
            )
            await message.reply("Okay,\n"
                               "I will use this image as custom thumbnail.. 🖐️",
                               reply_markup=InlineKeyboardMarkup(
                                   [[InlineKeyboardButton("Delete Thumbnail",
                                                  callback_data="deleteThumbnail")]]
                               ))
            return
        else:
            # Get Thumbnail from DB
            thumbnail=await db.get_thumbnail(message.from_user.id)
            if not thumbnail:
                await message.reply(
                                    "You didn't set custom thumbnail!\n"
                                    "reply /thumbnail to set thumbnail",
                                    quote=True
                                    )
                return
            await message.reply_photo(
                                     photo=thumbnail, caption="Custom Thumbnail",
                                     quote=True,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("Delete Thumbnail",
                                                  callback_data="deleteThumbnail")]]
                                     ))
            return
    except Exception:
        pass

geThumb=filters.create(lambda _, __, query: query.data=="getThumb")
addThumb=filters.create(lambda _, __, query: query.data=="addThumb")
delThumb=filters.create(lambda _, __, query: query.data=="delThumb")

@ILovePDF.on_callback_query(geThumb)
async def _getThumb(bot, callbackQuery):
    try:
        if not isMONGOexist:
            await callbackQuery.answer(
                                      "Can't Use This Feature 🤧"
                                      )
            return
        else:
            await callbackQuery.answer(
                                      "wait.! Let me think.. 🤔"
                                      )
            thumbnail=await db.get_thumbnail(callbackQuery.message.chat.id)
            if not thumbnail:
                try:
                    await callbackQuery.edit_message_media(PDF_THUMBNAIL)
                except Exception:
                    pass
                await callbackQuery.edit_message_caption(
                                                        caption="🌟 CURRENT THUMBNAIL 🌟 (DEFAULT)\n\n"
                                                                "You didn't set any custom thumbnail!\n\n"
                                                                "/thumbnail :to get current thumbnail"
                                                                "Reply to a photo to set custom thumbnail",
                                                        reply_markup=InlineKeyboardMarkup(
                                                            [[InlineKeyboardButton("😒 ADD THUMB 😒",
                                                                     callback_data="addThumb")],
                                                             [InlineKeyboardButton("« BACK «",
                                                                     callback_data="back")]]
                                                        ))
                return
            await callbackQuery.edit_message_media(str(thumbnail))
            await callbackQuery.edit_message_caption(
                                                    "🌟 CURRENT THUMBNAIL 🌟\n\n"
                                                            "/thumbnail :to get current thumbnail"
                                                            "Reply to a photo to set custom thumbnail",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        [[InlineKeyboardButton("🥲 CHANGE 🥲",
                                                                 callback_data="addThumb"),
                                                          InlineKeyboardButton("🤩 DELETE 🤩",
                                                                 callback_data="delThumb")],
                                                         [InlineKeyboardButton("« BACK «",
                                                                 callback_data="back")]]
                                                    ))
            return
    except Exception as e:
        await callbackQuery.message.reply(e)

@ILovePDF.on_callback_query(addThumb)
async def _addThumb(bot, callbackQuery):
    try:
        await callbackQuery.answer()
        await callbackQuery.edit_message_caption(
                                                caption="Now, Send me a Image..",
                                                reply_markup=InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("Waiting.. 🥱",
                                                             callback_data="noResponse")]]
                                                ))
        await asyncio.sleep(1)
        await callbackQuery.edit_message_caption(
                                                caption="Now, Send me a Image for Future Use.. 😅\n\n"
                                                        "Don't have enough time, send me fast 😏",
                                                reply_markup=InlineKeyboardMarkup(
                                                    [[InlineKeyboardButton("Waiting.. 🥱",
                                                             callback_data="noResponse")]]
                                                ))
        getThumb=await bot.listen(callbackQuery.from_user.id)
        if not getThumb.photo:
            await getThumb.delete()
        else:
            await callbackQuery.edit_media(getThumb.photo.file_id)
            await callbackQuery.edit_message_caption(
                                                    caption="🌟 CURRENT THUMBNAIL 🌟\n\n"
                                                            "/thumbnail :to get current thumbnail"
                                                            "Reply to a photo to set custom thumbnail",
                                                    reply_markup=InlineKeyboardMarkup(
                                                        [[InlineKeyboardButton("🥲 CHANGE 🥲",
                                                                 callback_data="addThumb"),
                                                          InlineKeyboardButton("🤩 DELETE 🤩",
                                                                 callback_data="delThumb")],
                                                         [InlineKeyboardButton("« BACK «",
                                                                 callback_data="back")]]
                                                    ))
            await db.set_thumbnail(
                                  callbackQuery.from_user.id,
                                  getThumb.photo.file_id
                                  )
            await getThumb.delete()
    except Exception:
        pass

@ILovePDF.on_callback_query(delThumb)
async def _delThumb(bot, callbackQuery):
    try:
        await callbackQuery.answer(
                                  "Deleted.. 😎"
                                  )
        await callbackQuery.edit_media(WELCOME_PIC)
        await _back(bot, callbackQuery)
        await db.set_thumbnail(callbackQuery.from_user.id, None)
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
