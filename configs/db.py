# fileName: Configs/db.py
# copyright ©️ 2021 nabilanavab

import os

isMONGOexist=os.environ.get("MONGODB_URI", False)
# if os.environ.get("MONGODB_URI", False):
#     isMONGOexist=True

LOG_CHANNEL=os.environ.get("LOG_CHANNEL", False)

BANNED_USR_DB, BANNED_GRP_DB = [], []

#--------------->
#--------> CONFIG VAR.
#------------------->

class dataBASE(object):
    # mongoDB Url (Optional)
    MONGODB_URI=os.environ.get("MONGODB_URI", False)

#                                                                             Telegram: @nabilanavab
