# fileName : plugins/dm/callBack/encrypt.py
# copyright ©️ 2021 nabilanavab

# import os
import fitz
from pyrogram.types import Message

#--------------->
#--------> LOCAL VARIABLES
#------------------->

encryptedFileCaption="Page Number : {}\nkey 🔐 : ||{}||"

#--------------->
#--------> PDF ENCRYPTION
#------------------->

async def encryptPDF(message_id, password):
    try:
        swd=f"abi"
        input_file=f"{message_id}/inPut.pdf"
        output_file=f"{message_id}/outPut.pdf"
        _pswd="n"+f"{swd}"+"l"
        
        with fitz.open(input_file) as encrptPdf:
            number_of_pages=encrptPdf.pageCount
            encrptPdf.save(
                output_pdf,
                # strongest algorithm
                encryption=fitz.PDF_ENCRYPT_AES_256,
                owner_pw=_pswd,
                user_pw=f"{password.text}",
                permissions=int(
                    fitz.PDF_PERM_ACCESSIBILITY |
                    fitz.PDF_PERM_PRINT |
                    fitz.PDF_PERM_COPY |
                    fitz.PDF_PERM_ANNOTATE
                )
            )
            return encryptedFileCaption.format(number_of_pages, password.text)
    except Exception as e:
        print("Encrypt: ", e)
        return False

#                                                                                  Telegram: @nabilanavab
