import discord
import MySQLdb
import numpy as np
import re
from mydblib import my_select

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)

dbName = "test_debt"


def registerToDB(id, creditor, debtor, amount):
    connect = MySQLdb.connect(
        host="localhost",
        user="root",
        password="kotaro0722",
        db=dbName
    )

    cursor = connect.cursor()

    sql_insert_data = f"INSERT INTO debt(id,creditor,debtor,amount,ispay) values({id},'{creditor}','{debtor}','{amount}',0)"
    cursor.execute(sql_insert_data)

    connect.commit()

    cursor.close()
    connect.close()


async def showAllCredit(creditor, message):
    sql_string = f"SELECT debtor,amount FROM debt WHERE creditor={creditor} AND ispay=0"
    data = my_select(dbName, sql_string)
    sum = data.groupby("debtor").sum(numeric_only=True)
    for i in range(len(sum)):
        await message.channel.send(f"<@{sum[i:i+1].index[0]}>:{sum[i:i+1]["amount"].iloc[-1]}円")

async def showOneCredit(creditor,debtor,message):
    sql_string=f"SELECT amount FROM debt WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data=my_select(dbName,sql_string)
    sum=data.sum(numeric_only=True)
    await message.channel.send(f"<@{debtor}>:{sum.iloc[-1]}円")

# def arrangeList(lists: list):
#     newLists = []
#     for list in lists:
#         l = list[0:2:1]
#         newLists.append(l)
#     return newLists


# def splitList(lists: list, members):
#     returnObject = {}
#     for list in lists:
#         counter = 0
#         for member in members:
#             if member == list[0]:
#                 counter += list[1]
#         returnObject[member] = counter
#     return returnObject


# def searchCheck(message: discord.Message):
#     pattern = "!"
#     repattern = re.compile(pattern)
#     result = repattern.match(message)
#     return result
#     # checker = False
#     # for phrase in message.content:
#     #     if phrase == "!":
#     #         checker = True
#     # return checker


# async def showHistory(isDebtor: bool, person, message, member):
    # data = 0
    # if isDebtor:
    #     data = showDebt(message.mentions[1].name)
    # else:
    #     data = showCredit(message.mentions[1].name)
    # arrangeData = arrangeList(data)
    # splitData = splitList(arrangeData, member)
    # await message.channel.send(splitData)
    # for datum in splitData:
    #     await message.channel.send(splitData[datum])


async def getMemberList(message):
    guild = client.get_guild(message.guild.id)
    members = guild._members
    memberList = []
    for member in members.values():
        # if not member.bot:
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


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content
    pattern_is_summon = "<@1095252448601456672>"
    is_summon = re.match(pattern_is_summon, message_content)
    if is_summon:
        pattern_is_debtor = pattern_is_summon+r"\s*"+await getDebtor(message)
        is_debtor = re.fullmatch(pattern_is_debtor, message_content)

        is_all_debt = re.fullmatch(pattern_is_summon, message_content)

        if is_all_debt:
            await showAllCredit(message.author.id, message)

        elif is_debtor:
            debtor = re.findall(r"[0-9]+",message_content)[1]
            await showOneCredit(message.author.id,debtor,message)
        else:
            await message.channel.send("不正な入力です")

    pattern_is_register = await getPatternIsRegister(message)
    is_register = re.fullmatch(pattern_is_register, message_content)
    if is_register:
        pattern_debtor_id = "[0-9]+"
        debtor = re.findall(pattern_debtor_id, message_content)[0]

        creditor = message.author.id

        pattern_amount = pattern_debtor_id
        amount = re.findall(pattern_amount, message_content)[1]

        id = message.id

        registerToDB(id, creditor, debtor, amount)
        await message.channel.send("登録できました")


@client.event
async def on_raw_reaction_add(payload):
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.member

    if (user == client.user):
        return

    msg = message.content
    await txt_channel.send(msg)

client.run(Token)
