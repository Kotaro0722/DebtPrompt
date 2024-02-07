import discord
import sqlite3
import re

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
# intents.reactions = True
# intents.guilds = True
client = discord.Client(intents=intents)

dbName = "DebtPrompt.db"


def registerToDB(creditor, debtor, amount, notes, id):
    connect = sqlite3.connect(dbName)
    cursor = connect.cursor()
    insert = """INSERT INTO debt(id,debtor, creditor, amount, detail, isRepay) VALUES(:id,:debtor, :creditor, :amount, :detail, :isRepay)"""
    insertList = {
        "id": id,
        "debtor": debtor,
        "creditor": creditor,
        "amount": amount,
        "detail": notes,
        "isRepay": 0
    }
    cursor.execute(insert, insertList)
    data = cursor.fetchall()
    connect.commit()
    connect.close()
    return data


def showDebt(debtor):
    connect = sqlite3.connect(dbName)
    cursor = connect.cursor()
    select = "SELECT creditor,amount,detail,isRepay FROM debt WHERE debtor=(:debtor) AND isRepay=(:isRepay)"
    selectList = {"debtor": debtor, "isRepay": 0}
    cursor.execute(select, selectList)
    data = cursor.fetchall()
    return data


def showCredit(creditor):
    connect = sqlite3.connect(dbName)
    cursor = connect.cursor()
    select = "SELECT creditor,amount,detail FROM debt WHERE creditor=(:creditor) AND isRepay=(:isRepay)"
    selectList = {"creditor": creditor, "isRepay": 0}
    cursor.execute(select, selectList)
    data = cursor.fetchall()
    return data


def arrangeList(lists: list):
    newLists = []
    for list in lists:
        l = list[0:2:1]
        newLists.append(l)
    return newLists


def splitList(lists: list, members):
    returnObject = {}
    for list in lists:
        counter = 0
        for member in members:
            if member == list[0]:
                counter += list[1]
        returnObject[member] = counter
    return returnObject


def searchCheck(message: discord.Message):
    pattern = "!"
    repattern = re.compile(pattern)
    result = repattern.match(message)
    return result
    # checker = False
    # for phrase in message.content:
    #     if phrase == "!":
    #         checker = True
    # return checker


async def showHistory(isDebtor: bool, person, message, member):
    data = 0
    if isDebtor:
        data = showDebt(message.mentions[1].name)
    else:
        data = showCredit(message.mentions[1].name)
    arrangeData = arrangeList(data)
    splitData = splitList(arrangeData, member)
    await message.channel.send(splitData)
    # for datum in splitData:
    #     await message.channel.send(splitData[datum])


async def getMember(message):
    guild = client.get_guild(message.guild.id)
    members = guild._members
    memberList = []
    for member in members.values():
        if not member.bot:
            memberList.append(member.id)
    return memberList


async def getDebtor(message):
    list_party = await getMember(message)
    pattern = ""
    for id in list_party:
        pattern += f"<@{id}> | "
    pattern = pattern.rstrip().rstrip("|").rstrip()
    return pattern


async def getPatternIsRegister(message):
    pattern = await getDebtor(message)
    pattern += "[\s]*[0-9]+円"
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
        debtor = message_content.replace(pattern_is_summon+" ", "", 1)
        pattern_is_debtor = await getDebtor(message)
        is_debtor = re.fullmatch(pattern_is_debtor, debtor)

        is_all_debt = re.fullmatch(pattern_is_summon, message_content)

        if is_all_debt:
            await message.channel.send("すべての債権を表示します。")

        elif not is_debtor:
            await message.channel.send("不正な入力です")
            return
        else:
            await message.channel.send("～～さんへの債権を表示します。")

    pattern_is_register = await getPatternIsRegister(message)
    is_register = re.match(pattern_is_register, message_content)
    if is_register:
        await message.channel.send("登録できました")
# @client.event
# async def on_reaction_add(reaction, user):
#     print("リアクションが付与されました。")

client.run(Token)
