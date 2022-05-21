# fileName : plugins/thumbName.py
# copyright ©️ 2021 nabilanavab

import os
from configs.db import isMONGOexist
from configs.images import DEFAULT_NAME
from configs.images import PDF_THUMBNAIL   # DEFAULT THUMBNAIL
from configs.images import CUSTOM_THUMBNAIL_U

if isMONGOexist:
    from database import db
if DEFAULT_NAME:
    newName=DEFAULT_NAME

# return thumbnail and fileName
async def thumbName(userID, fileName):
    
    fileNm, fileExt=os.path.splitext(fileName)
    if newName:
        DEFAULT_NAME=DEFAULT_NAME+fileExt
    
    # if no mongoDB return False [default thumbnail ]
    if not isMONGOexist:
        # id no DEFAULT_NAME, use current file name 
        if newName:
            return PDF_THUMBNAIL, DEFAULT_NAME
        else:
            return PDF_THUMBNAIL, fileName
    
    # user with thumbnail
    if userID in CUSTOM_THUMBNAIL_U:
        thumbnail=await db.get_thumbnail(userID)
        if newName:
            return thumbnail, DEFAULT_NAME
        else:
            return thumbnail, fileName
    
    # user without thumbnail
    else:
        if newName:
            return PDF_THUMBNAIL, DEFAULT_NAME
        else:
            return PDF_THUMBNAIL, fileName

#                                       Telegram: @nabilanavab
