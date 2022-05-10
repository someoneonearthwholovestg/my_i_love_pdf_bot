# fileName : plugins/dm/callBack/ocr.py
# copyright ©️ 2021 nabilanavab

# import os
from pyrogram.types import Message


try:
    nabilanavab=False # Change to False else never work
    import ocrmypdf
except Exception:
    nabilanavab=True

#--------------->
#--------> LOCAL VARIABLES
#------------------->

ocr="OCR PDF"

#--------------->
#--------> OCR PDF
#------------------->

async def ocrPDF(message, message_id):
    try:
        try:
            input_file=f"{message_id}/inPut.pdf"
            output_file=f"{message_id}/outPut.pdf"
            
            ocrmypdf.ocr(
                input_file=open(input_file, "rb"),
                output_file=open(output_file, "wb"),
                deskew=True
            )
            return ocr
        except Exception:
            await message.edit("`Already Have A Text Layer.. `😏")
            return False
    except Exception as e:
        print("ocr: " , e)
        return False

#                                                             Telegram: @nabilanavab
