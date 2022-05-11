# fileName : plugins/dm/callBack/decrypt.py
# copyright ©️ 2021 nabilanavab

# import os
import fitz
from pyrogram.types import Message

#--------------->
#--------> LOCAL VARIABLES
#------------------->

passwordError="__Cannot Decrypt the file with__ `{}` 🕸️"

decrypted="__Decrypted File__"

#--------------->
#--------> PDF DECRYPTION
#------------------->

async def decryptPDF(message, message_id, password):
    try:
        input_file=f"{message_id}/inPut.pdf"
        output_file=f"{message_id}/outPut.pdf"
        
        try:
            with fitz.open(input_file) as encrptPdf:
                encrptPdf.authenticate(f"{password.text}")
                encrptPdf.save(output_file)
                return decrypted
        except Exception:
            await message.edit(passwordError.format(password.text))
            return False
    except Exception as e:
        print("Decrypt: ", e)
        return False

#                                                                                  Telegram: @nabilanavab
