import discord
import sqlite3

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"
intents = discord.Intents.default()
intents.message_content = True
# intents.reactions = True
# intents.guilds = True
client = discord.Client(intents=intents)

dbName="DebtPrompt.db"

def registerToDB(creditor,messageList):
    [debtor,amount,notes]=messageList
    connect=sqlite3.connectect(dbName)
    cursor=connect.cursorsor()
    insert="""INSERT INTO debt(debtor,creditor,amount,detail,isPay) VALUES(:debtor,:creditor,:amount,:detail.:isPay)"""
    cursor.execute(insert,{
        "debtor":debtor,
        "creditor":creditor,
        "amount":amount,
        "detail":notes,
        "isPay":0
    })
    connect.commit()
    connect.close()
    
def showDebt(debtor):
    connect=sqlite3.connectect(dbName)
    cursor=connect.cursorsor()
    select="SELECT creditor,amount,detail,isRepay FROM debt WHERE debtor=(:debtor)"
    selectList={"debtor":debtor}
    cursor.execute(select,selectList)
    data=cursor.fetchall()
    return data
    
def showCredit(creditor):
    connect=sqlite3.connectect(dbName)
    cursor=connect.cursorsor()
    select="SELECT creditor,amount,detail,isRepay FROM debt WHERE creditor=(:creditor)"
    selectList={"creditor":creditor}
    cursor.execute(select,selectList)
    data=cursor.fetchall()
    return data

def arrangeList(lists:list):
    newLists=[]
    for list in lists:
        l=list(list)
        del l[2]
        newLists.append(l)
        
    
    
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author==client.user:
        return 
    messageList=message.channel.send(message.content.split())
    await registerToDB(message.autor,messageList)
    
    
client.run(Token)
