import discord
import mysql.connector as mydb
import numpy as np
import re
from db.db_select import my_select
from db.db_update import my_update
import config

Token = config.TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)

dbName = config.DBNAME
main_table = config.MAIN_TABLE

register_channel_id = config.REGISTER_CHANNEL_ID


def register_DB(id, creditor, debtor, amount, ispay):
    sql_insert_data = f"INSERT INTO {main_table}(id,creditor,debtor,amount,ispay) values({id},'{creditor}','{debtor}','{amount}',{ispay})"
    my_update(sql_insert_data)

def update_DB(id,creditor,debtor,amount,ispay):
    sql_update_data=f"INSERT INTO {main_table} (id,creditor,debtor,amount,ispay) VALUES ({id},'{creditor}','{debtor}',{amount},{ispay}) ON DUPLICATE KEY UPDATE debtor=VALUES(debtor), amount=VALUES(amount), ispay=VALUES(ispay);"
    my_update(sql_update_data)

def delete_DB(id):
    sql_delete_data=f"DELETE FROM {main_table} WHERE id={id};"
    my_update(sql_delete_data)

async def show_all_credit(creditor, message):
    sql_string = f"SELECT debtor,amount FROM {main_table} WHERE creditor={creditor} AND ispay=0"
    data = my_select(sql_string)
    sum = data.groupby("debtor").sum(numeric_only=True)
    for i in range(len(sum)):
        debtor_user = await client.fetch_user(sum[i:i+1].index[0])
        message_send = await message.channel.send(f"{debtor_user.mention}:{sum[i:i+1]['amount'].iloc[-1]}円")

        sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={sum[i:i+1].index[0]} AND ispay=0;"
        data = my_select(sql_string)
        create_total(message_send.id, data)


async def show_one_credit(creditor, debtor, message):
    sql_string = f"SELECT amount FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(sql_string)
    sum = data.sum(numeric_only=True)
    debtor_user=await client.fetch_user(debtor)
    message_send = await message.channel.send(f"{debtor_user.mention} {sum.iloc[-1]}円")

    sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(sql_string)
    create_total(message_send.id, data)


def create_total(message_id, debt_ids):
    for debt_id in debt_ids["id"].tolist():
        sql_string = f"INSERT INTO total (message_id,debt_id) VALUES ({message_id},{debt_id})"
        my_update(sql_string)


def get_member_list(message):
    guild = client.get_guild(message.guild.id)
    members = guild._members
    memberList = [member.id for member in members.values() if not member.bot]
    return memberList


def get_debtor(message):
    list_party = get_member_list(message)
    pattern = "("
    for id in list_party:
        pattern += f"<@{id}>|"
    pattern = pattern.rstrip("|")
    pattern += ")"
    return pattern


def get_pattern_is_register(message):
    pattern = get_debtor(message)
    pattern += r"\s*-?[0-9]+円(?:\s+.*|$)"
    return pattern


def pay_one_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=1 WHERE id={message_id}"
    my_update(sql_string)


async def pay_all_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    for i in range(len(data)):
        pay_one_debt(data.at[i, "debt_id"])
        message = await channel.fetch_message(data.at[i, "debt_id"])
        await message.add_reaction("✅")


def cancel_one_pay_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=0 WHERE id={message_id}"
    my_update(sql_string)


async def cancel_all_pay_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    for i in range(len(data)):
        cancel_one_pay_debt(data.at[i, "debt_id"])
        message = await channel.fetch_message(data.at[i, "debt_id"])
        await message.remove_reaction("✅", client.user)


async def scroll_message(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        pattern_for_register = get_pattern_is_register(message)
        for_register = re.fullmatch(pattern_for_register, message.content)
        if not message.author.bot and for_register:
            is_register = False
            is_pay = 0
            for reaction in message.reactions:
                if reaction.emoji == "⭕" and reaction.me:
                    is_register = True
                if reaction.emoji == "✅":
                    is_pay = 1
            if not is_register:
                pattern_debtor_id = "[0-9]+"
                debtor = re.findall(pattern_debtor_id, message.content)[0]
                amount = re.findall(pattern_debtor_id, message.content)[1]
                register_DB(message.id, message.author.id,
                             debtor, amount, is_pay)
            await message.add_reaction("⭕")


async def show_detail(message_id: discord.Message, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    for i in range(len(data)):
        await channel.send(f"[その{i+1}](<https://discord.com/channels/963060474646257675/1098819625346682981/{data.at[i,'debt_id']}>)")


async def delete_circle(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        try:
            await message.remove_reaction("⭕")
        except Exception as e:
            print(e)

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
    else:
        await message.channel.send("不正な入力です")


    pattern_is_register = get_pattern_is_register(message)
    is_register = re.fullmatch(pattern_is_register, message.content)
    if is_register:
        pattern_debtor_id = "-?[0-9]+"
        debtor = re.findall(pattern_debtor_id, message.content)[0]

        creditor = message.author.id

        pattern_amount = pattern_debtor_id
        amount = re.findall(pattern_amount, message.content)[1]

        id = message.id

        register_DB(id, creditor, debtor, amount, 0)
        await message.add_reaction("⭕")

@client.event
async def on_raw_message_edit(payload:discord.RawMessageUpdateEvent):
    guild=await client.fetch_guild(payload.guild_id)
    channel=await guild.fetch_channel(payload.channel_id)
    message=await channel.fetch_message(payload.data["id"])
    author=payload.data["author"]["id"]
    if author==client.user:
        return

    message.content=message.content

    pattern_is_update = get_pattern_is_register(message)
    is_update=re.fullmatch(pattern_is_update,message.content)
    if is_update:
        id=message.id
        creditor=author
        debtor,amount=re.match(r"<@(\d+)>\s+(\d+)円",message.content).groups()
        ispay=any(reaction.emoji=="✅" for reaction in message.reactions)
        update_DB(id,creditor,debtor,amount,ispay)

@client.event
async def on_raw_message_delete(payload:discord.RawMessageDeleteEvent):
    delete_DB(payload.message_id)

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
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
        await show_detail(payload.message_id, txt_channel)


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
