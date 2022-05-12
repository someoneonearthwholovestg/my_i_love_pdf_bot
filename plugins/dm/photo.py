# fileName : Plugins/dm/photo.py
# copyright ©️ 2021 nabilanavab

import os
from pdf import PDF
from PIL import Image
from pdf import invite_link
from pyrogram import filters
from Configs.dm import Config
from pyrogram import Client as ILovePDF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

UPDATE_CHANNEL=Config.UPDATE_CHANNEL

#--------------->
#--------> LOCAL VARIABLES
#------------------->

imageAdded = """`Added {} page/'s to your pdf..`🤓

/generate to generate PDF 🤞"""

forceSubMsg = """Wait [{}](tg://user?id={})..!!

Due To The Huge Traffic Only Channel Members Can Use this Bot 🚶

This Means You Need To Join The Below Mentioned Channel for Using Me!

hit on "retry ♻️" after joining.. 😅"""

# PIC="./IMAGES/start.jpeg"
PIC="https://te.legra.ph/file/50c4d6e580ed98d931549.jpg"

#--------------->
#--------> REPLY TO IMAGES
#------------------->

@ILovePDF.on_message(filters.private & ~filters.edited & filters.photo)
async def images(bot, message):
    try:
        global invite_link
        await message.reply_chat_action("typing")
        # CHECK USER IN CHANNEL (IF UPDATE_CHANNEL ADDED)
        if UPDATE_CHANNEL:
            try:
                userStatus=await bot.get_chat_member(str(UPDATE_CHANNEL), message.chat.id)
                # IF USER BANNED FROM CHANNEL
                if userStatus.status=='banned':
                     await message.reply_photo(
                         photo=PIC, quote=True,
                         caption="For Some Reason You Can't Use This Bot"
                                 "\n\nContact Bot Owner 🤐",
                         reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Owner 🎊", url="https://t.me/nabilanavab")]]
                         )
                     )
                     return
            except Exception:
                if invite_link==None:
                    invite_link=await bot.create_chat_invite_link(int(UPDATE_CHANNEL))
                await message.reply_photo(
                    photo=PIC, quote=True,
                    caption=forceSubMsg.format(
                        message.from_user.first_name, message.chat.id
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("🌟 JOIN CHANNEL 🌟", url=invite_link.invite_link)
                        ],[
                            InlineKeyboardButton("Refresh ♻️", callback_data="refresh")
                        ]]
                    )
                )
                return
        imageReply=await message.reply_text("`Downloading your Image..⏳`", quote=True)
        if not isinstance(PDF.get(message.chat.id), list):
            PDF[message.chat.id]=[]
        await message.download(
            f"{message.chat.id}/{message.chat.id}.jpg"
        )
        img=Image.open(
            f"{message.chat.id}/{message.chat.id}.jpg"
        ).convert("RGB")
        PDF[message.chat.id].append(img)
        await imageReply.edit(
            imageAdded.format(len(PDF[message.chat.id]))
        )
    except Exception:
        pass

#                                                                                  Telegram: @nabilanavab
