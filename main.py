import discord
import re
from db.db_update import my_update
import config
from main_db import register_DB, update_DB, delete_DB
from bot_client import client
from main_credit import show_all_credit, show_one_credit, show_detail
from main_pay import pay_one_debt, pay_all_debt, cancel_one_pay_debt, cancel_all_pay_debt
from main_message import get_member_list, get_register_pattern, parse_register_message, scroll_message, delete_circle


Token = config.TOKEN

dbName = config.DBNAME
main_table = config.MAIN_TABLE

register_channel_id = config.REGISTER_CHANNEL_ID


# Botが起動した際に呼ばれる
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    debt_table_create_sql="""
        CREATE TABLE IF NOT EXISTS debt(
            `id` BIGINT PRIMARY KEY,
            `creditor` BIGINT,
            `debtor` BIGINT,
            `amount` INT,
            `ispay` BOOLEAN
        )"""
    my_update(debt_table_create_sql)
    total_table_create_sql="""
        CREATE TABLE IF NOT EXISTS total(
            `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
            `message_id` BIGINT,
            `debt_id` BIGINT
        )"""
    my_update(total_table_create_sql)


# ユーザがメッセージを送信したときに呼ばれる
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    is_all_debt=re.fullmatch(f"<@{client.user.id}>",message.content)

    # 自分に債権がある借金を全て表示
    if is_all_debt:
        await show_all_credit(message.author.id,message)

    # 自分に債権がある借金のうち指定された債務者の分を表示
    elif re.fullmatch(fr"<@{client.user.id}>\s*(?:<@(\d+)>\s*)+",message.content):
        ids=re.findall(r"<@(\d+)>",message.content)
        ids.remove(str(client.user.id))

        channel_member= get_member_list(message)
        is_only_user=all(int(id) in channel_member for id in ids)
        if is_only_user:
            for id in ids:
                await show_one_credit(message.author.id, id, message)

    # 履歴の読み取り
    elif re.fullmatch(fr"<@{client.user.id}>\s*scroll",message.content):
        register_channel = client.get_channel(int(register_channel_id))
        await scroll_message(register_channel)

    # ⭕リアクションの削除
    elif re.fullmatch(fr"<@{client.user.id}>\s*delete",message.content):
        register_channel = client.get_channel(int(register_channel_id))
        await delete_circle(register_channel)

    # 間違ったコマンドへのメッセージ
    elif re.search(rf"<@{client.user.id}>",message.content):
        await message.add_reaction("🤖")
        await message.add_reaction("❌")

    elif re.fullmatch(await get_register_pattern(message), message.content):
        id=message.id
        creditor=message.author.id
        debtor,amount=parse_register_message(message.content)
        register_DB(id, creditor, debtor, amount, 0)
        await message.add_reaction("⭕")

# ユーザがメッセージを編集したときに呼ばれる
@client.event
async def on_raw_message_edit(payload:discord.RawMessageUpdateEvent):
    author=payload.data["author"]["id"]
    if author==client.user:
        return

    guild=await client.fetch_guild(payload.guild_id)
    channel=await guild.fetch_channel(payload.channel_id)
    message=await channel.fetch_message(payload.data["id"])

    message.content=message.content

    pattern_is_update = await get_register_pattern(message,guild)
    is_update=re.fullmatch(pattern_is_update,message.content)
    if is_update:
        id=message.id
        creditor=author
        debtor,amount=parse_register_message(message.content)
        ispay=any(reaction.emoji=="✅" for reaction in message.reactions)
        update_DB(id,creditor,debtor,amount,ispay)
        await message.add_reaction("⭕")
    else:
        await message.remove_reaction("⭕",client.user)


# ユーザがメッセージを削除したときに呼ばれる
@client.event
async def on_raw_message_delete(payload:discord.RawMessageDeleteEvent):
    delete_DB(payload.message_id)

# ユーザがリアクションを付けたときに呼ばれる
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    guild=await client.fetch_guild(payload.guild_id)
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.user_id

    if user == client.user:
        return

    if message.author.id != payload.user_id and message.author.id != client.user.id:
        return

    if payload.emoji.name == "✅":
        if list(filter(lambda rea: rea.emoji == "✅", message.reactions))[0].me:
            await message.remove_reaction("✅", client.user)
            return

        register_channel = client.get_channel(int(register_channel_id))
        if message.author.id == client.user.id:
            await pay_all_debt(message.id, register_channel)
        else:
            pay_one_debt(message.id)

    if payload.emoji.name == "❔" and client.user.id == message.author.id:
        debtor=await guild.fetch_member(re.match(r"<@(\d+)>",message.content).group(1))
        await show_detail(message,debtor, txt_channel,payload)

# ユーザがリアクションを消したときに呼ばれる
@client.event
async def on_raw_reaction_remove(payload):
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.member

    if user == client.user:
        return

    if message.author.id != payload.user_id and message.author.id != client.user.id:
        return

    if payload.emoji.name != "✅":
        return

    register_channel = client.get_channel(int(register_channel_id))
    if message.author.id == client.user.id:
        await cancel_all_pay_debt(message.id, register_channel)
    else:
        cancel_one_pay_debt(message.id)

client.run(Token)
