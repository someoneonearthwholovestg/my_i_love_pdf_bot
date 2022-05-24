# fileName: Configs/group.py
# copyright ©️ 2021 nabilanavab

import os

#--------------->
#--------> CONFIG VAR.
#------------------->

class groupConfig(object):
    
    # add admins Id list by space seperated (Optional)
    ONLY_GROUP=list(set(int(x) for x in os.environ.get("ONLY_GROUP", "").split()))
    
    # banned groups can't use this bot (Optional)
    BANNED_GROUP=list(set(int(x) for x in os.environ.get("BANNED_USERS", "0").split()))
    if not BANNED_GROUP:
        BANNED_GROUP=[]

#                                                                             Telegram: @nabilanavab
