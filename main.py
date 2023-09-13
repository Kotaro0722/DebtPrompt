import discord

Token = "MTA5NTI1MjQ0ODYwMTQ1NjY3Mg.GjaVkI.k8OJ16DqLE1SxwHSoCiXrz20oVF5agg3JtzfOY"
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_raw_reaction_add(payload):
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.member
    if (message.author == user):
        return

    msg = f"{message.author.mention} {payload.emoji}\nFrom:{user.display_name} \
          \nMessage:{message.content}\n{message.jump_url}"

    CHANNEL_ID = 1095253848391700652
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(msg)

client.run(Token)
