import discord
import re
import main_db


# メッセージが送られたサーバーに存在するBot以外のユーザのリスト
async def get_member_list(message,guild=None):
    members = message.guild.members if not guild else  [member async for member in guild.fetch_members()]
    memberList = [member.id for member in members if not member.bot]
    return memberList

# 借金のフォーマットを作成する
async def get_register_pattern(message,guild=None):
    ids=await get_member_list(message,guild)
    pattern = r"(?:"+"|".join(re.escape(f"<@{id}>") for id in ids)+r")\s*-?[0-9]+円(?:\s+.*|$)"
    return pattern

# Discordのチャンネル上に残された履歴をDBに取り込む
async def scroll_message(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        pattern_for_register = await get_register_pattern(message)
        for_register = re.fullmatch(pattern_for_register, message.content)
        if not message.author.bot and for_register:
            is_register = False
            is_pay = 0
            for reaction in message.reactions:
                if reaction.emoji == "⭕" and reaction.me:
                    is_register = True
                if reaction.emoji == "✅":
                    is_pay = 1
            if not is_register:
                pattern_debtor_id = "[0-9]+"
                debtor = re.findall(pattern_debtor_id, message.content)[0]
                amount = re.findall(pattern_debtor_id, message.content)[1]
                main_db.register_DB(message.id, message.author.id,
                             debtor, amount, is_pay)
            await message.add_reaction("⭕")

# DBに取り込んだ証である⭕リアクションを消す
async def delete_circle(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        try:
            await message.remove_reaction("⭕")
        except Exception as e:
            print(e)
