# fileName : plugins/thumbName.py
# copyright ©️ 2021 nabilanavab

# LOGGING INFO: DEBUG
import logging
logger=logging.getLogger(__name__)
logging.basicConfig(
                   level=logging.DEBUG,
                   format="%(levelname)s:%(name)s:%(message)s" # %(asctime)s:
                   )

import os
from pdf import app
from PIL import Image
from pyrogram import Client
from pyrogram.types import Message
from configs.db import isMONGOexist
from configs.images import DEFAULT_NAME
from configs.images import PDF_THUMBNAIL   # DEFAULT THUMBNAIL
from configs.images import CUSTOM_THUMBNAIL_U

# THUMBNAIL METADATA
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

if isMONGOexist:
    from database import db

changeNAME=False
if DEFAULT_NAME:
   changeNAME=True

# return thumbnail height
async def thumbMeta(thumbPath: str):
    try:
        metadata = extractMetadata(createParser(thumbPath))
        if metadata.has("height"):
            return metadata.get("height")
        else:
            return 0
    except Exception as e:
        logger.exception(
                        "THUMB_META:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# photo_id -> local image
async def localThumb(photoID, messageID):
    try:
        location = await app.download_media(
                                message=photoID ,
                                file_name=f"{messageID}Thumb.jpeg",
                                )
        height = await thumbMeta(location)
        Image.open(thumb_path).convert("RGB").save(location)
        img = Image.open(location)
        img.resize((320, height))
        img.save(location, "JPEG")
        return location
    except Exception as e:
        logger.exception(
                        "LOCAL_THUMB:CAUSES %(e)s ERROR",
                        exc_info=True
                        )

# return thumbnail and fileName
async def thumbName(message, fileName):
    try:
        fileNm, fileExt = os.path.splitext(fileName)
        if changeNAME:
            DEFAULT_NAME = DEFAULT_NAME + fileExt
        
        # if no mongoDB return False [default thumbnail ]
        if not isMONGOexist:
            # id no DEFAULT_NAME, use current file name 
            if changeNAME:
                return PDF_THUMBNAIL, DEFAULT_NAME
            else:
                return PDF_THUMBNAIL, fileName
        
        # user with thumbnail
        if message.chat.id in CUSTOM_THUMBNAIL_U:
            thumbnail = await db.get_thumbnail(message.chat.id)
            thumbLoc = await localThumb(thumbnail, message.message_id)
            if changeNAME:
                return thumbLoc, DEFAULT_NAME
            else:
                return thumbnail, fileName
        
        # user without thumbnail
        else:
            if changeNAME:
                return PDF_THUMBNAIL, DEFAULT_NAME
            else:
                return PDF_THUMBNAIL, fileName
    
    except Exception as e:
        logger.exception(
                        "THUMB_NAME:CAUSES %(e)s ERROR",
                        exc_info=True
                        )


#                                                         Telegram: @nabilanavab
