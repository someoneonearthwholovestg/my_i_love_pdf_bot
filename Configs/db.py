# fileName: Configs/db.py
# copyright ©️ 2021 nabilanavab

import os
import database

#--------------->
#--------> CONFIG VAR.
#------------------->

BANNED_USR_DB, BANNED_GRP_DB = [], []

class dataBASE(object):
    
    isMONGOexist=False
    # mongoDB Url (Optional)
    MONGODB_URI=os.environ.get("MONGODB_URI", False)
    if MONGODB_URI:
        isMONGOexist=True
        userBANNED_db, groupBANNED_db=await db.get_banned()
        BANNED_USR_DB=userBANNED_db
        BANNED_GRP_DB=groupBANNED_db
    
    LOG_CHANNEL=os.environ.get("LOG_CHANNEL", False)

#                                                                             Telegram: @nabilanavab