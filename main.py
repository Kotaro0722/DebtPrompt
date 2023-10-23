import discord
import sqlite3

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"
intents = discord.Intents.default()
intents.message_content = True
# intents.reactions = True
# intents.guilds = True
client = discord.Client(intents=intents)

dbName = "DebtPrompt.db"


def registerToDB(creditor, messageList):
    [debtor, amount, notes] = messageList
    debtor[1:]
    connect = sqlite3.connect(dbName)
    cursor = connect.cursor()
    insert = """INSERT INTO debt(debtor, creditor, amount, detail, isRepay) VALUES(:debtor, :creditor, :amount, :detail, :isRepay)"""
    insertList = {
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


def getCreditor(message: discord.Message):
    guild = client.get_guild(message.guild.id)
    messageList = message.content.split()
    creditorID = messageList[0][3:len(messageList[0])-1]
    userNickname = guild.get_member(1095253731102179352)
    return guild


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # registerToDB(message.author.name, messageList)
    debtor = getCreditor(message)
    await message.channel.send(debtor)


client.run(Token)
