# by:koala @mixiologist
# One Piece
from telethon.events import ChatAction
from userbot import ALIVE_NAME, CMD_HELP, bot
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from userbot.events import register
from telethon.tl.types import MessageEntityMentionName


async def get_full_user(event):
    args = event.pattern_match.group(1).split(':', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Sensei, Ini Tidak Akan Mungkin Tanpa ID Pengguna`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("`Terjadi Kesalahan... Mohon Lapor Ke Grup` @LordUserbot_Group", str(err))
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj
# Ported For One-Piece by @coklintoud


@bot.on(ChatAction)
async def handler(tele):
    if tele.user_joined or tele.user_added:
        try:
            from userbot.modules.sql_helper.gmute_sql import is_gmuted

            guser = await tele.get_user()
            gmuted = is_gmuted(guser.id)
        except BaseException:
            return
        if gmuted:
            for i in gmuted:
                if i.sender == str(guser.id):
                    chat = await tele.get_chat()
                    admin = chat.admin_rights
                    creator = chat.creator
                    if admin or creator:
                        try:
                            await client.edit_permissions(
                                tele.chat_id, guser.id, view_messages=False
                            )
                            await tele.reply(
                                f"**Sensei, Pengguna Gban Ini Telah Bergabung** \n"
                                f"**Pengguna**: [{guser.id}](tg://user?id={guser.id})\n"
                                f"**Aksi**  : `Banned`"
                            )
                        except BaseException:
                            return


@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("`Sensei Ingin Menggunakan Perintah Global Banned!`")
    else:
        dark = await dc.edit("`Memproses Global Banned Pengguna Ini ヅ`")
    me = await userbot.client.get_me()
    await dark.edit(f"`𝙶𝚕𝚘𝚋𝚊𝚕 𝚋𝚊𝚗𝚗𝚎𝚍 𝚊𝚔𝚊𝚗 𝚜𝚎𝚐𝚎𝚛𝚊 𝚊𝚔𝚝𝚒𝚏, 𝚊𝚗𝚍𝚊 𝚊𝚔𝚊𝚗 𝚍𝚒 𝚋𝚊𝚗𝚗𝚎𝚍 𝚘𝚕𝚎𝚑 𝚜𝚎𝚗𝚜𝚊𝚒 𝚔𝚊𝚛𝚎𝚗𝚊 𝚔𝚎𝚜𝚊𝚕𝚊𝚑𝚊𝚗 𝚏𝚊𝚝𝚊𝚕 𝚊𝚗𝚍𝚊 🔥`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit(f"`Terjadi Kesalahan Sensei`")
    if user:
        if user.id == 1269122778:
            return await dark.edit(
                f"`Anda Tidak Akan Bisa Melakukan Global Banned Ke Sensei Shadow, Dia Adalah Pembuat Saya 😔`"
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except BaseException:
            pass
        try:
            await userbot.client(BlockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await dark.edit(f"`Global Banned Aktif ✅`")
            except BaseException:
                b += 1
    else:
        await dark.edit(f"`Sensei Replay Pesannya`")
    try:
        if gmute(user.id) is False:
            return await dark.edit(f"**Kesalahan! Pengguna Ini Sudah Kena Perintah Global Banned Sensei.**")
    except BaseException:
        pass
    return await dark.edit(
        f"**🗡 𝐏𝐞𝐫𝐢𝐧𝐭𝐚𝐡 𝐬𝐞𝐧𝐬𝐞𝐢:** `{ALIVE_NAME}`\n**⚰ 𝐏𝐞𝐧𝐠𝐠𝐮𝐧𝐚:** [{user.first_name}](tg://user?id={user.id})\n**🩸 𝐀𝐤𝐬𝐢:** `Global Banned`"
    )


@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def gunben(userbot):
    dc = userbot
    sender = await dc.get_sender()
    me = await dc.client.get_me()
    if not sender.id == me.id:
        dark = await dc.reply("`Membatalkan Perintah Global Banned Pengguna Ini `")
    else:
        dark = await dc.edit("`Membatalkan Perintah Global Banned `")
    me = await userbot.client.get_me()
    await dark.edit(f"`𝙼𝚎𝚖𝚞𝚕𝚊𝚒 𝚖𝚎𝚕𝚎𝚙𝚊𝚜 𝚙𝚎𝚛𝚒𝚗𝚝𝚊𝚑 𝚐𝚕𝚘𝚋𝚊𝚕 𝚋𝚊𝚗𝚗𝚎𝚍, 𝚙𝚎𝚗𝚐𝚐𝚞𝚗𝚊 𝚒𝚗𝚒 𝚊𝚔𝚊𝚗 𝚍𝚊𝚙𝚊𝚝 𝚋𝚎𝚛𝚐𝚊𝚋𝚞𝚗𝚐 𝚕𝚊𝚐𝚒 𝚔𝚎 𝚐𝚛𝚞𝚙 𝚊𝚗𝚍𝚊 𝚜𝚎𝚗𝚜𝚎𝚒 🩸`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await dark.edit("`Terjadi Kesalahan ヅ`")
    if user:
        if user.id == 1353102497:
            return await dark.edit("**Sensei Pengguna Tidak Bisa Terkena Perintah Ini, Karna Dia Pembuatku **")
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass
        try:
            await userbot.client(UnblockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await dark.edit(f"`Membatalkan Global Banned... Memproses... `")
            except BaseException:
                b += 1
    else:
        await dark.edit("`Harap Balas Ke Pesan Pengguna Sensei😡`")
    try:
        if ungmute(user.id) is False:
            return await dark.edit("**Kesalahan! Pengguna Sedang Tidak Di Global Banned.**")
    except BaseException:
        pass
    return await dark.edit(
        f"**🔥 𝐏𝐞𝐫𝐢𝐧𝐭𝐚𝐡 𝐬𝐞𝐧𝐬𝐞𝐢:** `{ALIVE_NAME}`\n**🔥 𝐏𝐞𝐧𝐠𝐠𝐮𝐧𝐚:** [{user.first_name}](tg://user?id={user.id})\n**🔥 𝐀𝐤𝐬𝐢:** `Membatalkan Global Banned`"
    )


CMD_HELP.update({
    "gban": "\
`.gban`\
\nUsage: Melakukan Banned Secara Global Ke Semua Grup Dimana Sensei Sebagai Admin.\
\n\n`.ungban`\
\nUsage: Membatalkan Global Banned"
})
