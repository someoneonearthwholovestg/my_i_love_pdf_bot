# fileName : plugins/dm/callBack/pdfcallB.py
# copyright ©️ 2021 nabilanavab

from pdf import PROCESS
from pyrogram import filters
from pyrogram import Client as ILovePDF
from plugins.fileSize import get_size_format as gSF
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--------------->
#--------> LOCAL VARIABLES
#------------------->

pdfReply=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⭐ META£ATA ⭐", callback_data="pdfInfo"),
                InlineKeyboardButton("🗳️ PREVIEW 🗳️", callback_data="preview")
            ],[
                InlineKeyboardButton("🖼️ IMAGES 🖼️", callback_data="toImage"),
                InlineKeyboardButton("✏️ TEXT ✏️", callback_data="toText")
            ],[
                InlineKeyboardButton("🔐 ENCRYPT 🔐", callback_data="encrypt"),
                InlineKeyboardButton("🔓 DECRYPT 🔓", callback_data="decrypt")
            ],[
                InlineKeyboardButton("🗜 COMPRESS 🗜️", callback_data="compress"),
                InlineKeyboardButton("🤸 ROTATE 🤸", callback_data="rotate")
            ],[
                InlineKeyboardButton("✂️ SPLIT ✂️", callback_data="split"),
                InlineKeyboardButton("🧬 MERGE 🧬", callback_data="merge")
            ],[
                InlineKeyboardButton("™️ STAMP ™️", callback_data="stamp"),
                InlineKeyboardButton("✏️ RENAME ✏️", callback_data="rename")
            ],[
                InlineKeyboardButton("📝 OCR 📝", callback_data="ocr"),
                InlineKeyboardButton("🥷 A4 FORMAT 🥷", callback_data="format")
            ],[
                InlineKeyboardButton("🚫 CLOSE 🚫",callback_data="closeALL")
            ]
        ]
    )

BTPMcb="""`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`"""

KBTPMcb="""`What shall i wanted to do with this file.?`

File Name: `{}`
File Size: `{}`

`Number of Pages: {}`✌️"""

#--------------->
#--------> LOCAL VARIABLES
#------------------->

"""
______VARIABLES______

I : as image
D : as document
K : pgNo known
A : Extract All
R : Extract Range
S : Extract Single page
BTPM : back to pdf message
KBTPM : back to pdf message (known pages)

"""

#--------------->
#--------> PDF TO IMAGES (CB/BUTTON)
#------------------->

BTPM=filters.create(lambda _, __, query: query.data=="BTPM")
toImage=filters.create(lambda _, __, query: query.data=="toImage")
KBTPM=filters.create(lambda _, __, query: query.data.startswith("KBTPM|"))
KtoImage=filters.create(lambda _, __, query: query.data.startswith("KtoImage|"))

I=filters.create(lambda _, __, query: query.data=="I")
D=filters.create(lambda _, __, query: query.data=="D")
KI=filters.create(lambda _, __, query: query.data.startswith("KI|"))
KD=filters.create(lambda _, __, query: query.data.startswith("KD|"))

zIp=filters.create(lambda _, __, query: query.data=="zip")
KzIp=filters.create(lambda _, __, query: query.data.startswith("Kzip|"))

tAr=filters.create(lambda _, __, query: query.data=="tar")
KtAr=filters.create(lambda _, __, query: query.data.startswith("Ktar|"))

rotate=filters.create(lambda _, __, query: query.data=="rotate")
Krotate=filters.create(lambda _, __, query: query.data.startswith("Krotate|"))

toText=filters.create(lambda _, __, query: query.data=="toText")
KtoText=filters.create(lambda _, __, query: query.data.startswith("KtoText|"))

error=filters.create(lambda _, __, query: query.data=="error")
closeme=filters.create(lambda _, __, query: query.data=="closeme")
closeALL=filters.create(lambda _, __, query: query.data=="closeALL")
underDev=filters.create(lambda _, __, query: query.data=="underDev")
canceled=filters.create(lambda _, __, query: query.data=="canceled")
completed=filters.create(lambda _, __, query: query.data=="completed")
cancelP2I=filters.create(lambda _, __, query: query.data=="cancelP2I")
notEncrypted=filters.create(lambda _, __, query: query.data=="notEncrypted")


# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(I)
async def _I(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » as Img » Pages: \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data="IA")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data="IR")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data="IS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="toImage")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo (with unknown pdf page number)
@ILovePDF.on_callback_query(D)
async def _D(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » as Doc » Pages: \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data="DA")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data="DR")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data="DS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="toImage")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KI)
async def _KI(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » as Img » Pages: \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🙄 Extract All 🙄", callback_data=f"KIA|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🤧 With In Range 🤧", callback_data=f"KIR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🌝 Single Page 🌝", callback_data=f"KIS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KtoImage|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo (with known pdf page number)
@ILovePDF.on_callback_query(KD)
async def _KD(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » as Doc » Pages: \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🙄 Extract All 🙄", callback_data=f"KDA|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🤧 With In Range 🤧", callback_data=f"KDR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🌝 Single Page 🌝", callback_data=f"KDS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KtoImage|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toImage)
async def _toImage(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Send pdf Images as:\nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🖼 IMG 🖼", callback_data="I"),
                        InlineKeyboardButton("📂 DOC 📂", callback_data="D")
                    ],[
                        InlineKeyboardButton("🤐 ZIP 🤐", callback_data="zip"),
                        InlineKeyboardButton("🎯 TAR 🎯", callback_data="tar")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception:
        pass

# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoImage)
async def _KtoImage(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Send pdf Images as:\nTotal pages: {number_of_pages}__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🖼 IMG 🖼️", callback_data=f"KI|{number_of_pages}"),
                        InlineKeyboardButton("📂 DOC 📂", callback_data=f"KD|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🤐 ZIP 🤐", callback_data=f"Kzip|{number_of_pages}"),
                        InlineKeyboardButton("🎯 TAR 🎯", callback_data=f"Ktar|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# back to pdf message (unknown page number)
@ILovePDF.on_callback_query(BTPM)
async def _BTPM(bot, callbackQuery):
    try:
        fileName=callbackQuery.message.reply_to_message.document.file_name
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        
        await callbackQuery.edit_message_text(
            BTPMcb.format(
                fileName, await gSF(fileSize)
            ),
            reply_markup=pdfReply
        )
    except Exception:
        pass

# Extract pgNo as Zip(with unknown pdf page number)
@ILovePDF.on_callback_query(tAr)
async def _tar(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » as Tar » Pages: \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data="tarA")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data="tarR")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data="tarS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo as Zip(with known pdf page number)
@ILovePDF.on_callback_query(KtAr)
async def _Ktar(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » as Tar» Pages: \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data=f"KtarA|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data=f"KtarR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data=f"KtarS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass


# Extract pgNo as Zip(with unknown pdf page number)
@ILovePDF.on_callback_query(zIp)
async def _zip(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf - Img » as Zip » Pages: \nTotal pages: unknown__ 😐",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data="zipA")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data="zipR")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data="zipS")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data="BTPM")
                    ]
                ]
            )
        )
    except Exception:
        pass

# Extract pgNo as Zip(with known pdf page number)
@ILovePDF.on_callback_query(KzIp)
async def _Kzip(bot, callbackQuery):
    try:
        _, number_of_pages = callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf - Img » as Zip» Pages: \nTotal pages: {number_of_pages}__ 🌟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Extract All 🙄", callback_data=f"KzipA|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("With In Range 🙂", callback_data=f"KzipR|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("Single Page 🌝", callback_data=f"KzipS|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                    ]
                ]
            )
        )
    except Exception:
        pass

# back to pdf message (with known page Number)
@ILovePDF.on_callback_query(KBTPM)
async def _KBTPM(bot, callbackQuery):
    try:
        fileName=callbackQuery.message.reply_to_message.document.file_name
        fileSize=callbackQuery.message.reply_to_message.document.file_size
        
        _, number_of_pages=callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            KBTPMcb.format(
                fileName, await gSF(fileSize), number_of_pages
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⭐ META£ATA ⭐", callback_data=f"KpdfInfo|{number_of_pages}"),
                        InlineKeyboardButton("🗳️ PREVIEW 🗳️", callback_data="Kpreview")
                    ],[
                        InlineKeyboardButton("🖼️ IMAGES 🖼️", callback_data=f"KtoImage|{number_of_pages}"),
                        InlineKeyboardButton("✏️ TEXT ✏️", callback_data=f"KtoText|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🔐 ENCRYPT 🔐", callback_data=f"Kencrypt|{number_of_pages}"),
                        InlineKeyboardButton("🔓 DECRYPT 🔓", callback_data=f"notEncrypted")
                    ],[
                        InlineKeyboardButton("🗜️ COMPRESS 🗜️", callback_data=f"Kcompress"),
                        InlineKeyboardButton("🤸 ROTATE 🤸", callback_data=f"Krotate|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("✂️ SPLIT ✂️", callback_data=f"Ksplit|{number_of_pages}"),
                        InlineKeyboardButton("🧬 MERGE 🧬", callback_data="merge")
                    ],[
                        InlineKeyboardButton("™️ STAMP ™️", callback_data=f"Kstamp|{number_of_pages}"),
                        InlineKeyboardButton("✏️ RENAME ✏️", callback_data="rename")
                    ],[
                        InlineKeyboardButton("📝 OCR 📝", callback_data=f"Kocr|{number_of_pages}"),
                        InlineKeyboardButton("🥷 A4 FORMAT 🥷", callback_data=f"Kformat|{number_of_pages}")
                    ],[
                        InlineKeyboardButton("🚫 CLOSE 🚫", callback_data="closeALL")
                    ]
                ]
            )
        )
    except Exception:
        pass


# rotate PDF (unknown pg no)
@ILovePDF.on_callback_query(rotate)
async def _rotate(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Total Pages: Unknown 😐\nRotate PDF in :__",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("90°", callback_data="rot90"),
                    InlineKeyboardButton("180°", callback_data="rot180")
                ],[
                    InlineKeyboardButton("270°", callback_data="rot270"),
                    InlineKeyboardButton("360°", callback_data="rot360")
                ],[
                    InlineKeyboardButton("« Back «", callback_data="BTPM")
                ]]
            )
        )
    except Exception:
        pass

# rotate PDF (only change in back button)
@ILovePDF.on_callback_query(Krotate)
async def _Krotate(bot, callbackQuery):
    try:
        _, number_of_pages=callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Total Pages: {number_of_pages} 🌟\nRotate PDF in:__",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("90°", callback_data="rot90"),
                    InlineKeyboardButton("180°", callback_data="rot180")
                ],[
                    InlineKeyboardButton("270°", callback_data="rot270"),
                    InlineKeyboardButton("360°", callback_data="rot360")
                ],[
                    InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                ]]
            )
        )
    except Exception:
        pass

# pdf to images (with unknown pdf page number)
@ILovePDF.on_callback_query(toText)
async def _toText(bot, callbackQuery):
    try:
        await callbackQuery.edit_message_text(
            "__Pdf » Text\nTotal Pages: unknown 😐\nNow, Specify the format:__",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Messages 📜", callback_data="M"),
                    InlineKeyboardButton("Txt file 🧾", callback_data="T")
                ],[
                    InlineKeyboardButton("Html 🌐", callback_data="H"),
                    InlineKeyboardButton("Json 🎀", callback_data="J")
                ],[
                    InlineKeyboardButton("« Back «", callback_data="BTPM")
                ]]
            )
        )
    except Exception:
        pass

# pdf to images (with known page Number)
@ILovePDF.on_callback_query(KtoText)
async def _KtoText(bot, callbackQuery):
    try:
        _, number_of_pages=callbackQuery.data.split("|")
        await callbackQuery.edit_message_text(
            f"__Pdf » Text\nTotal pages: {number_of_pages} 🌟         \nNow, Specify the format:__",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Messages 📜", callback_data="KM"),
                    InlineKeyboardButton("Txt file 🧾", callback_data="KT")
                ],[
                    InlineKeyboardButton("Html 🌐", callback_data="KH"),
                    InlineKeyboardButton("Json 🎀", callback_data="KJ")
                ],[
                    InlineKeyboardButton("« Back «", callback_data=f"KBTPM|{number_of_pages}")
                ]]
            )
        )
    except Exception:
        pass

@ILovePDF.on_callback_query(underDev)
async def _underDev(bot, callbackQuery):
    try:
        await callbackQuery.answer("This feature is Under Development ⛷️")
    except Exception:
        pass

# Error in Codec
@ILovePDF.on_callback_query(error)
async def _error(bot, callbackQuery):
    try:
        await callbackQuery.answer("Error annenn paranjille.. then what.. 😏")
    except Exception:
        pass

# Download Cancel 
@ILovePDF.on_callback_query(closeme)
async def _closeme(bot, callbackQuery):
    try:
        try:
            await callbackQuery.message.delete()
        except Exception:
            pass
        await callbackQuery.answer("Process Canceled.. 😏")
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception:
        pass

# File Not Encrypted callBack
@ILovePDF.on_callback_query(notEncrypted)
async def _notEncrypted(bot, callbackQuery):
    try:
        await callbackQuery.answer("File Not Encrypted.. 👀")
    except Exception:
        pass

# Close both Pdf Message + CB
@ILovePDF.on_callback_query(closeALL)
async def _closeALL(bot, callbackQuery):
    try:
        await callbackQuery.message.delete()
        await callbackQuery.message.reply_to_message.delete()
    except Exception:
        pass

# Cancel Pdf to Images, Images to Zip
@ILovePDF.on_callback_query(cancelP2I)
async def _cancelP2I(bot, callbackQuery):
    try:
        await callbackQuery.message.edit_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("💤 CANCELLING.. 💤", callback_data="n")]])
        )
        PROCESS.remove(callbackQuery.message.chat.id)
    except Exception:
        pass

@ILovePDF.on_callback_query(canceled)
async def _canceled(bot, callbackQuery):
    try:
        await callbackQuery.answer("Nothing Official About it.. 😅")
    except Exception:
        pass

@ILovePDF.on_callback_query(completed)
async def _completed(bot, callbackQuery):
    try:
        await callbackQuery.answer("🎉 Completed.. 🏃")
    except Exception:
        pass

#                                                                                             Telegram: @nabilanavab
