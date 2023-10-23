import discord
import sqlite3
import re

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"
intents = discord.Intents.default()
intents.message_content = True
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
    connect = sqlite3.connectect(dbName)
    cursor = connect.cursorsor()
    select = "SELECT creditor,amount,detail,isRepay FROM debt WHERE debtor=(:debtor) isRepay=(:isRepay)"
    selectList = {"debtor": debtor, "isRepay": 0}
    cursor.execute(select, selectList)
    data = cursor.fetchall()
    return data


def showCredit(creditor):
    connect = sqlite3.connectect(dbName)
    cursor = connect.cursorsor()
    select = "SELECT creditor,amount,detail,isRepay FROM debt WHERE creditor=(:creditor) isRepay=(:isRepay)"
    selectList = {"creditor": creditor, "isRepay": 0}
    cursor.execute(select, selectList)
    data = cursor.fetchall()
    return data


def arrangeList(lists: list):
    newLists = []
    for list in lists:
        l = list(list)
        del l[2]
        newLists.append(l)
    return newLists


def splitList(lists: list, members: list):
    returnObject = {}
    for list in lists:
        counter = 0
        for member in members:
            if member == list[0]:
                counter += list[1]
        returnObject[member] = counter
    return returnObject


def searchCheck(message: discord.Message):
    checker = False
    for phrase in message.content:
        if phrase == "!":
            checker = True
    return checker


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    messageList = message.content.split()

    debtor = message.mentions[0].name
    # registerToDB(message.author.name, debtor,
    #              messageList[1], messageList[2], message.id)

    for mention in message.mentions:
        if mention.name == "借金催促":
            if searchCheck(message):
                showDebt(message.mentions[1].name)


client.run(Token)
