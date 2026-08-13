import config
from db.db_select import my_select
from db.db_update import my_update
from bot_client import client


main_table = config.MAIN_TABLE
register_channel_id = config.REGISTER_CHANNEL_ID

# ある債権者の全ての債権を表示する
async def show_all_credit(creditor, message):
    sql_string = f"SELECT debtor,amount FROM {main_table} WHERE creditor={creditor} AND ispay=0"
    data = my_select(sql_string)
    sum = data.groupby("debtor").sum(numeric_only=True)
    for i in range(len(sum)):
        debtor_user = await client.fetch_user(sum[i:i+1].index[0])
        message_send = await message.channel.send(f"{debtor_user.mention}:{sum[i:i+1]['amount'].iloc[-1]}円")

        sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={sum[i:i+1].index[0]} AND ispay=0;"
        data = my_select(sql_string)
        create_total(message_send.id, data)

# ある債権者のうち、一人分の債権を表示する
async def show_one_credit(creditor, debtor, message):
    sql_string = f"SELECT amount FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(sql_string)
    sum = data.sum(numeric_only=True)
    debtor_user=await client.fetch_user(debtor)
    message_send = await message.channel.send(f"{debtor_user.mention} {sum.iloc[-1]}円")

    sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(sql_string)
    create_total(message_send.id, data)

# 現時点でのある債権者の所有する債権を債務者ごとに合計する
def create_total(message_id, debt_ids):
    for debt_id in debt_ids["id"].tolist():
        sql_string = f"INSERT INTO total (message_id,debt_id) VALUES ({message_id},{debt_id})"
        my_update(sql_string)

# 合計された債権の詳細を確認する
async def show_detail(message, debtor, channel, payload):
    sql_string = f"SELECT * FROM total WHERE message_id={message.id}"
    data = my_select(sql_string)

    for i in range(len(data)):
        await channel.send(f"[{debtor.display_name}:その{i+1}](<https://discord.com/channels/{payload.guild_id}/{register_channel_id}/{data.at[i,'debt_id']}>)")
