import discord
import numpy as np
import re
import config
from debtManager import debt_manager_on_message ,debt_manager_on_raw_reaction_add,debt_manager_on_raw_reaction_remove

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
    await debt_manager_on_message(message,client)

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await debt_manager_on_raw_reaction_add(payload,client)

@client.event
async def on_raw_reaction_remove(payload):
    await debt_manager_on_raw_reaction_remove(payload,client)

client.run(Token)
