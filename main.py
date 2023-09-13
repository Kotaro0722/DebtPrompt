import discord
import sqlite3

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"
intents = discord.Intents.default()
intents.message_content = True
# intents.reactions = True
# intents.guilds = True
client = discord.Client(intents=intents)

dbName="debt.db"

def useDB(creditor,messageList):
    [debtor,amount,notes]=messageList
    conn=sqlite3.connect(dbName)
    cur=conn.cursor()
    cur.execute("create table debtPrompt(creditor STRING,debtor STRING,amount INTEGER,notes STRING)")
    cur.execute("insert into debtPrompt(creditor) values("+creditor+")")
    cur.execute("insert into debtPrompt(debtor) values("+debtor+")")
    cur.execute("insert into debtPrompt(amount) values("+amount+")")
    cur.execute("insert into debtPrompt(notes) values("+notes+")")
    conn.commit()
    conn.close()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author==client.user:
        return 
    messageList=message.channel.send(message.content.split())
    await useDB(message.autor,messageList)
    
    
client.run(Token)
