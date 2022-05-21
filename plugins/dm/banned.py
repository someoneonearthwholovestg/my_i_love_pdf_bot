# fileName : plugins/dm/banned.py
# copyright ©️ 2021 nabilanavab

import os
from asyncio import sleep
from pyrogram import filters
from pyrogram.types import (
                           InlineKeyboardButton,
                           InlineKeyboardMarkup
                           )
from configs.dm import Config
from configs.db import isMONGOexist
from configs.db import BANNED_USR_DB
from pyrogram import Client as ILovePDF
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid

if isMONGOexist:
    from database import db


@ILovePDF.on_message(
                    filters.incoming &
                    filters.command('ban') &
                    filters.private & filters.user(Config.ADMINS)
                    )
async def _banUser(bot, message):
    try:
        if not isMONGOexist:
            await message.reply(
                               "Sry, Bot Don't have a DB",
                               quote=True
                               )
            return
        procs=await message.reply(
                                 "⚙️ Processing..",
                                 quote=True
                                 )
        await sleep(2)
        if len(message.command)==1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM=message.text.split(None)
        if len(reM)>2:
            chat=message.text.split(None, 2)[1]
            reason=message.text.split(None, 2)[2]
        else:
            chat=message.command[1]
            reason="oru rasam 😏"
        try:
            chat=int(chat)
        except Exception: # if username [Exception]
            pass
        try:
            userINFO=await bot.get_users(chat)
        except PeerIdInvalid:
            return await procs.edit(
                                   "This is an invalid user, make sure ia have met him before.."
                                   )
        except IndexError:
            return await procs.edit(
                                   "This might be a channel, make sure its a user.."
                                   )
        except Exception as e:
            return await procs.edit(
                                   f"Error: `{e}`"
                                   )
        else:
            if userINFO.id==531733867:
                return await procs.edit(
                                       f"Before Banning {userINFO.mention}.!\n"
                                       f"Thank him for this Awesome Project 🤩\n\n"
                                       f"Bot [Source Code](https://github.com/nabilanavab/iLovePDF) 😲"
                                       )
            elif (userINFO.id in Config.ADMINS):
                return await procs.edit(
                                       f"I Never Ban {userINFO.mention}.. \n"
                                       "Reason: iCantBanBotADMIN 😏"
                                       )
            status=await db.get_ban_status(userINFO.id)
            if status['is_banned']:
                return await procs.edit(
                                       f"{userINFO.mention} is already banned\n"
                                       f"Reason: {status['ban_reason']}"
                                       )
            await db.ban_user(userINFO.id, reason)
            BANNED_USR_DB.append(userINFO.id)
            await procs.edit(
                            f"Successfully banned {userINFO.mention}"
                            )
    except Exception as e:
        await procs.edit(e)


@ILovePDF.on_message(
                    filters.incoming &
                    filters.command('unban') &
                    filters.private & filters.user(Config.ADMINS)
                    )
async def _unbanUser(bot, message):
    try:
        if not isMONGOexist:
            await message.reply(
                               "Sry, Bot Don't have a DB",
                               quote=True
                               )
            return
        procs=await message.reply(
                           "⚙️ Processing",
                           quote=True
                           )
        await sleep(2)
        if len(message.command)==1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM=message.text.split(None)
        if len(reM)>2:
            chat=message.text.split(None, 2)[1]
            reason=message.text.split(None, 2)[2]
        else:
            chat=message.command[1]
            reason="No reason Provided"
        try:
            chat=int(chat)
        except Exception:
            pass
        try:
            userINFO=await bot.get_users(chat)
        except PeerIdInvalid:
            return await procs.edit(
                                   "This is an invalid user, make sure ia have met him before.."
                                   )
        except IndexError:
            return await procs.edit(
                                   "This might be a channel, make sure its a user.."
                                   )
        except Exception as e:
            return await procs.edit(
                                   f"Error: `{e}`"
                                   )
        else:
            status=await db.get_ban_status(userINFO.id)
            if not status['is_banned']:
                return await procs.edit(
                                       f"{userINFO.mention} is not yet banned."
                                       )
            await db.remove_ban(userINFO.id)
            BANNED_USR_DB.remove(userINFO.id)
            await procs.edit(
                            f"Successfully unbanned {userINFO.mention}"
                            )
    except Exception as e:
        await procs.edit(e)


@ILovePDF.on_message(
                    filters.private &
                    filters.command('users') &
                    filters.user(Config.ADMINS) & filters.incoming
                    )
async def _listUser(bot, message):
    try:
        if not isMONGOexist:
            await message.reply(
                               "Sry, Bot Don't have a DB",
                               quote=True
                               )
            return
        procs=await message.reply(
                                "Getting List Of Users"
                                )
        await sleep(2)
        users=await db.get_all_users()
        out="Users Saved In DB Are:\n\n"
        await procs.edit(out)
        await sleep(2)
        async for user in users:
            out += f"[{user['name']}](tg://user?id={user['id']})"
            if user['ban_status']['is_banned']:
                out += '( Banned User )'
            out += '\n'
        try:
            await procs.edit(out)
        except MessageTooLong:
            await procs.delete()
            with open('users.txt', 'w+') as outfile:
                outfile.write(out)
            await message.reply_document(
                                        'users.txt',
                                        caption="List Of Users",
                                        quote=True
                                        )
            os.remove("users.txt")
    except Exception:
        pass


banUser=filters.create(lambda _, __, query: query.data.startswith("banU|"))

@ILovePDF.on_callback_query(banUser)
async def _banUserCB(bot, callbackQuery):
    try:
        if callbackQuery.from_user.id not in Config.admin:
            return await callbackQuery.answer(
                                             "Lesham Ulupp.."
                                             )
        _, userID=callbackQuery.data.split("|")
        if int(userID)==531733867:
            return await callbackQuery.answer(
                                             f"Don't Even Think about banning\n"
                                             f"𝙽𝙰𝙱𝙸𝙻  𝙰  𝙽𝙰𝚅𝙰𝙱\n"
                                             f"He's the master brain behind this project 😎"
                                             )
        elif int(userID) in Config.ADMINS:
            return await callbackQuery.answer(
                                             f"I Never Ban Him.. 😏\n"
                                             "Reason: iCantBanBotADMIN"
                                             )
            if callbackQuery.from_user.id in BANNED_USR_DB:
                return await callbackQuery.answer(
                                                 f"He is already banned\n"
                                                 )
            await db.ban_user(callbackQuery.from_user.id, "oru rasam.. 😝")
            BANNED_USR_DB.append(callbackQuery.from_user.id)
            await callbackQuery.answer(
                                      f"Successfully banned Him 😎"
                                      )
            return await callbackQuery.message.edit_reply_markup(
                         InlineKeyboardMarkup(
                                 [[
                                         InlineKeyboardButton(
                                                 "» UnB@n »",
                                                 callback_data=f"unbanU|{callbackQuery.from_user.id}"
                                                 )
                                 ]]
                         ))
    except Exception:
        pass


#                                                                                          Telegram: @nabilanavab
