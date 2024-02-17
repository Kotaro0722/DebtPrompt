import discord
import MySQLdb
import numpy as np
import re
from mydblib import my_select
from mydblib2 import my_update

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)

dbName = "test_debt"
main_table="debt"

register_channel_id=1150109427182096394

def registerToDB(id, creditor, debtor, amount):
    connect = MySQLdb.connect(
        host="localhost",
        user="root",
        password="kotaro0722",
        db=dbName
    )

    cursor = connect.cursor()

    sql_insert_data = f"INSERT INTO {main_table}(id,creditor,debtor,amount,ispay) values({id},'{creditor}','{debtor}','{amount}',0)"
    cursor.execute(sql_insert_data)

    connect.commit()

    cursor.close()
    connect.close()

async def showAllCredit(creditor, message):
    sql_string = f"SELECT debtor,amount FROM {main_table} WHERE creditor={creditor} AND ispay=0"
    data = my_select(dbName, sql_string)
    sum = data.groupby("debtor").sum(numeric_only=True)
    for i in range(len(sum)):
        message_send=await message.channel.send(f"<@{sum[i:i+1].index[0]}>:{sum[i:i+1]["amount"].iloc[-1]}円")
        
        sql_string=f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={sum[i:i+1].index[0]} AND ispay=0;"
        data=my_select(dbName,sql_string)
        createNewTable(message_send.id,data)

async def showOneCredit(creditor, debtor, message):
    sql_string = f"SELECT amount FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(dbName, sql_string)
    sum = data.sum(numeric_only=True)
    message_send= await message.channel.send(f"<@{debtor}>:{sum.iloc[-1]}円")
    
    sql_string=f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data=my_select(dbName,sql_string)
    createNewTable(message_send.id,data)

def createNewTable(message_id,data):
    sql_string=f"CREATE TABLE sum_{message_id}(id VARCHAR(20) PRIMARY KEY);"
    my_update(dbName,sql_string)
    for i in range(len(data)):
        sql_insert_data = f"INSERT INTO sum_{message_id}(id) values({data.at[i,"id"]});"
        my_update(dbName,sql_insert_data)

async def getMemberList(message):
    guild = client.get_guild(message.guild.id)
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
    sql_string=f"UPDATE {main_table} SET ispay=1 WHERE id={message_id}"
    my_update(dbName,sql_string) 
    
async def payAllDebt(message_id,channel):
    sql_string=f"SELECT * FROM sum_{message_id}"
    data=my_select(dbName,sql_string)
    for i in range(len(data)):
        payOneDebt(data.at[i,"id"])
        message= await channel.fetch_message(data.at[i,"id"])
        await message.add_reaction("✅")
    
def cancelOnePayDebt(message_id):
    sql_string=f"UPDATE {main_table} SET ispay=0 WHERE id={message_id}"
    my_update(dbName,sql_string)

async def cancelAllPayDebt(message_id,channel):
    sql_string=f"SELECT * FROM sum_{message_id}"
    data=my_select(dbName,sql_string)
    for i in range(len(data)):
        cancelOnePayDebt(data.at[i,"id"])
        message= await channel.fetch_message(data.at[i,"id"])
        await message.remove_reaction("✅",client.user)
    
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
            debtor = re.findall(r"[0-9]+", message_content)[1]
            await showOneCredit(message.author.id, debtor, message)
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
    user = payload.user_id
    
    if user == client.user:
        return
    
    if message.author.id!=payload.user_id and message.author.id!=client.user.id:
        return 

    if payload.emoji.name!="✅":
        return
    
    if list(filter(lambda rea:rea.emoji=="✅",message.reactions))[0].me:
        await message.remove_reaction("✅",client.user)
        return
    
    register_channel=client.get_channel(register_channel_id)
    if message.author.id==client.user.id :
        await payAllDebt(message.id,register_channel)
    else :
        payOneDebt(message.id)
    
@client.event
async def on_raw_reaction_remove(payload):
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.member

    if user == client.user:
        return
    
    if message.author.id!=payload.user_id and message.author.id!=client.user.id:
        return 

    if payload.emoji.name!="✅":
        return
    
    register_channel=client.get_channel(register_channel_id)
    if message.author.id==client.user.id :
        await cancelAllPayDebt(message.id,register_channel)
    else :
        cancelOnePayDebt(message.id)
    
client.run(Token)
