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
    for i in range(len(data)):
        pay_one_debt(data.at[i, "debt_id"])
        message = await channel.fetch_message(data.at[i, "debt_id"])
        await message.add_reaction("✅")

# ある債権者が所有していて回収済みとなっていた一つの債権を復活する
def cancel_one_pay_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=0 WHERE id={message_id}"
    my_update(sql_string)

# ある債権者が所有していて回収済みとなっていた一人の債務者に対する債権を復活する
async def cancel_all_pay_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    for i in range(len(data)):
        cancel_one_pay_debt(data.at[i, "debt_id"])
        message = await channel.fetch_message(data.at[i, "debt_id"])
        await message.remove_reaction("✅", client.user)
