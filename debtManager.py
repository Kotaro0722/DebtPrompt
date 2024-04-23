import discord
import re
import mysql.connector as mydb
from mydblib import my_select
from mydblib2 import my_update
import config
import main

dbName = config.DBNAME
main_table = config.MAIN_TABLE

register_channel_id = config.REGISTER_CHANNEL_ID

def registerToDB(id, creditor, debtor, amount, ispay):
    connect = mydb.connect(
        host=config.HOST,
        user=config.USER,
        password=config.PASSWORD,
        db=dbName
    )

    cursor = connect.cursor(dictionary=True)

    sql_insert_data = f"INSERT INTO {main_table}(id,creditor,debtor,amount,ispay) values({id},'{creditor}','{debtor}','{amount}',{ispay})"
    cursor.execute(sql_insert_data)

    connect.commit()

    cursor.close()
    connect.close()


async def showAllCredit(creditor, message):
    sql_string = f"SELECT debtor,amount FROM {main_table} WHERE creditor={creditor} AND ispay=0"
    data = my_select(dbName, sql_string)
    sum = data.groupby("debtor").sum(numeric_only=True)
    for i in range(len(sum)):
        message_send = await message.channel.send(f"<@{sum[i:i+1].index[0]}>:{sum[i:i+1]['amount'].iloc[-1]}円")

        sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={sum[i:i+1].index[0]} AND ispay=0;"
        data = my_select(dbName, sql_string)
        createNewTable(message_send.id, data)


async def showOneCredit(creditor, debtor, message):
    sql_string = f"SELECT amount FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(dbName, sql_string)
    sum = data.sum(numeric_only=True)
    message_send = await message.channel.send(f"<@{debtor}>:{sum.iloc[-1]}円")

    sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(dbName, sql_string)
    createNewTable(message_send.id, data)


def createNewTable(message_id, data):
    sql_string = f"CREATE TABLE sum_{message_id}(id VARCHAR(20) PRIMARY KEY);"
    my_update(dbName, sql_string)
    for i in range(len(data)):
        sql_insert_data = f"INSERT INTO sum_{message_id}(id) values({data.at[i,'id']});"
        my_update(dbName, sql_insert_data)


async def getMemberList(message):
    guild = main.client.get_guild(message.guild.id)
    members = guild._members
    memberList = []
    for member in members.values():
        if not member.bot:
            memberList.append(member.id)
    return memberList


async def getDebtor(message):
    list_party = await getMemberList(message)
    pattern = "("
    for id in list_party:
        pattern += f"<@{id}>|"
    pattern = pattern.rstrip("|")
    pattern += ")"
    return pattern


async def getPatternIsRegister(message):
    pattern = await getDebtor(message)
    pattern += r"\s*[0-9]+円\s*.*"
    return pattern


def payOneDebt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=1 WHERE id={message_id}"
    my_update(dbName, sql_string)


async def payAllDebt(message_id, channel):
    sql_string = f"SELECT * FROM sum_{message_id}"
    data = my_select(dbName, sql_string)
    for i in range(len(data)):
        payOneDebt(data.at[i, "id"])
        message = await channel.fetch_message(data.at[i, "id"])
        await message.add_reaction("✅")


def cancelOnePayDebt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=0 WHERE id={message_id}"
    my_update(dbName, sql_string)


async def cancelAllPayDebt(message_id, channel):
    sql_string = f"SELECT * FROM sum_{message_id}"
    data = my_select(dbName, sql_string)
    for i in range(len(data)):
        cancelOnePayDebt(data.at[i, "id"])
        message = await channel.fetch_message(data.at[i, "id"])
        await message.remove_reaction("✅", main.client.user)


async def scrollMessage(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        pattern_for_register = await getPatternIsRegister(message)
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
                registerToDB(message.id, message.author.id,
                             debtor, amount, is_pay)
            await message.add_reaction("⭕")


async def showDetail(message_id: discord.Message, channel):
    sql_string = f"SELECT * FROM sum_{message_id}"
    data = my_select(dbName, sql_string)
    for i in range(len(data)):
        await channel.send(f"[その{i+1}](<https://discord.com/channels/963060474646257675/1098819625346682981/{data.at[i,'id']}>)")
