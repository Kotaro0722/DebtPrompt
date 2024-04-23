import discord
import numpy as np
import re
import config
from debtManager import getDebtor,showAllCredit,showOneCredit,register_channel_id,scrollMessage,getPatternIsRegister,registerToDB,payAllDebt,payOneDebt,showDetail,cancelAllPayDebt,cancelOnePayDebt

Token = config.TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    message_content = message.content
    pattern_is_summon = f"<@{client.user.id}>"
    is_summon = re.match(pattern_is_summon, message_content)
    if is_summon:
        pattern_is_debtor = pattern_is_summon+r"\s*"+await getDebtor(message)
        is_debtor = re.fullmatch(pattern_is_debtor, message_content)

        is_all_debt = re.fullmatch(pattern_is_summon, message_content)

        pattern_is_scroll = f"<@{client.user.id}>"+r"\s*"+"scroll"
        is_scroll = re.fullmatch(pattern_is_scroll, message_content)

        if is_all_debt:
            await showAllCredit(message.author.id, message)

        elif is_debtor:
            debtor = re.findall(r"[0-9]+", message_content)[1]
            await showOneCredit(message.author.id, debtor, message)

        elif is_scroll:
            register_channel = client.get_channel(int(register_channel_id))
            await scrollMessage(register_channel)

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

        registerToDB(id, creditor, debtor, amount, 0)
        await message.add_reaction("⭕")


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
            await payAllDebt(message.id, register_channel)
        else:
            payOneDebt(message.id)

    if payload.emoji.name == "❔" and client.user.id == message.author.id:
        await showDetail(payload.message_id, txt_channel)


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
        await cancelAllPayDebt(message.id, register_channel)
    else:
        cancelOnePayDebt(message.id)

client.run(Token)
