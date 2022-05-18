# fileName: plugins/dm/banned.py
# copyright ©️ 2021 nabilanavab

import os
from asyncio import sleep
from pyrogram import filters
from configs.dm import Config
from configs.db import isMONGOexist
from pyrogram import Client as ILovePDF
from pyrogram.errors import ChatAdminRequired
from plugins.dm.admin import BANNED_USR_DB, BANNED_GRP_DB
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
        sleep(1)
        if len(message.command)==1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM=message.text.split(None)
        if len(reM)>2:
            chat=int(message.text.split(None, 2)[1])
            reason=message.text.split(None, 2)[2]
        else:
            chat=int(message.command[1])
            reason="oru rasam 😏"
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
        sleep(1)
        if len(message.command)==1:
            return await procs.edit(
                                   "Give me a user id / username"
                                   )
        reM=message.text.split(None)
        if len(reM)>2:
            chat=int(message.text.split(None, 2)[1])
            reason=message.text.split(None, 2)[2]
        else:
            chat=int(message.command[1])
            reason="No reason Provided"
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
                            f"Successfully unbanned {k.mention}"
                            )
    except Exception:
        pass


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
        sleep(1)
        users=await db.get_all_users()
        out="Users Saved In DB Are:\n\n"
        await procs.edit(out)
        sleep(1)
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
