import discord
import config
from db.db_select import my_select
from db.db_update import my_update
from bot_client import client


main_table = config.MAIN_TABLE

# ある債権を回収する
def pay_one_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=1 WHERE id={message_id}"
    my_update(sql_string)

# ある債権者の所有する債権のうち、一人の債務者に関する債権を回数する
async def pay_all_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    debt_ids = data["debt_id"].tolist() if len(data) else []
    # 先にDBを全て更新する(リアクション付与の失敗で残りの債権が未回収のまま残らないようにする)
    for debt_id in debt_ids:
        pay_one_debt(debt_id)
    for debt_id in debt_ids:
        await _change_check_reaction(channel, debt_id, add=True)

# ある債権者が所有していて回収済みとなっていた一つの債権を復活する
def cancel_one_pay_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=0 WHERE id={message_id}"
    my_update(sql_string)

# ある債権者が所有していて回収済みとなっていた一人の債務者に対する債権を復活する
async def cancel_all_pay_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    debt_ids = data["debt_id"].tolist() if len(data) else []
    for debt_id in debt_ids:
        cancel_one_pay_debt(debt_id)
    for debt_id in debt_ids:
        await _change_check_reaction(channel, debt_id, add=False)

# 債権の登録メッセージに✅を付ける/外す
# 登録メッセージが別チャンネルにある・削除済みなどで失敗しても、他のメッセージの処理は続ける
async def _change_check_reaction(channel, debt_id, add):
    try:
        message = await channel.fetch_message(debt_id)
        if add:
            await message.add_reaction("✅")
        else:
            await message.remove_reaction("✅", client.user)
    except discord.HTTPException as e:
        print(f"登録メッセージ(id={debt_id})のリアクション変更に失敗\n{e}")
