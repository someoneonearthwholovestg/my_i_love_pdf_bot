# fileName : plugins/dm/callBack/compress.py
# copyright ©️ 2021 nabilanavab

import os
from pyrogram.types import Message
from plugins.fileSize import get_size_format as gSF
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet

#--------------->
#--------> LOCAL VARIABLES
#------------------->

compressedCaption="""`Original Size : {}
Compressed Size : {}

Ratio : {:.2f} %`"""

cantCompressMore="File Can't be Compressed More..🤐"

#--------------->
#--------> PDF COMPRESSION
#------------------->

async def compressPDF(message, message_id):
    try:
        input_file=f"{message_id}/inPut.pdf"
        output_file=f"{message_id}/outPut.pdf"
        
        # Initialize the library
        PDFNet.Initialize()
        doc=PDFDoc(input_file)
        # Optimize PDF with the default settings
        doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and
        # compressing data streams
        Optimizer.Optimize(doc)
        doc.Save(
            output_file, SDFDoc.e_linearized
        )
        doc.Close()
        
        # FILE SIZE COMPARISON (RATIO)
        initialSize=os.path.getsize(input_file)
        compressedSize=os.path.getsize(output_file)
        ratio=(1-(compressedSize/initialSize))*100
        
        # sends only if compressed more than 10mb or ratio >= 5%
        if True:#compressedSize>1000000 or ratio>=5:
            await message.edit("hi")
            return "compressedCaption" #.format(
                   # await gSF(initialSize), await gSF(compressedSize), ratio
               # )
        else:
            await message.edit(cantCompressMore)
            return False
    
    except Exception as e:
        await message.edit(f"❌SOMETHING WENT WRONG❌\nError: {e}")
        print("Compress: ", e)
        return False

#                                                                                  Telegram: @nabilanavab
