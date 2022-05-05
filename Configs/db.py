# fileName: Configs/db.py
# copyright ©️ 2021 nabilanavab

import os

isMONGOexist=False
if os.environ.get("MONGODB_URI", False):
    isMONGOexist=True

import database

#--------------->
#--------> CONFIG VAR.
#------------------->

class dataBASE(object):
    
    # mongoDB Url (Optional)
    MONGODB_URI=os.environ.get("MONGODB_URI", False)
    if MONGODB_URI:
        userBANNED_db, groupBANNED_db = db.get_banned()
        BANNED_USR_DB=userBANNED_db
        BANNED_GRP_DB=groupBANNED_db
    
    LOG_CHANNEL=os.environ.get("LOG_CHANNEL", False)

#                                                                             Telegram: @nabilanavab
