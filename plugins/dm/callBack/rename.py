# fileName : plugins/dm/callBack/rename.py
# copyright ©️ 2021 nabilanavab

#--------------->
#--------> LOCAL VARIABLES
#------------------->

renameCap="New Name: `{}`"

#--------------->
#--------> RENAME PDF
#------------------->

# Not Using, Just for Caption
async def rename(newName):
    try:
        # ADDS .pdf IF DONT HAVE AN EXTENSION
        # if newName.text[-4:]==".pdf":
        #     newName=newName.text
        # else:
        #     newName=newName.text + ".pdf"
        return renameCap.format(newName)
    except Exception as e:
        print("Rename: ",e)
        return False

#                                                                                  Telegram: @nabilanavab
