import discord
import re
import datetime
import mysql.connector as mydb
import config

task_table = config.TASK_TABLE


async def register_task(message):
    this_year = datetime.date.today().year
    date_str = re.findall(r"\d\d?/\d\d?\s\d\d?:\d\d", message)[0]
    date = datetime.datetime.strptime(
        f"{this_year}/"+date_str, "%Y/%m/%d %H:%M")
    thread_id = await message.fetch_thread().id
    print(thread_id)
    # connect = mydb.connect(
    #     host=config.HOST,
    #     user=config.USER,
    #     password=config.PASSWORD,
    #     db=config.DBNAME
    # )
    # cursor = connect.cursor(dictionary=True)

    # sql_insert_data = f"INSERT INTO {
    #     task_table}(message_id,thread_id,deadline) values({message.id},{thread_id}.{date})"
    # cursor.execute(sql_insert_data)
    # connect.commit()
    # cursor.close()
    # connect.close()


def task_manager_on_message(message: discord.Message, client: discord.Client):
    pattern_task_register = r"【.*】\s*[\d\d?/\d\d?\s\d\d?:\d\d]"
    is_task_register = re.fullmatch(pattern_task_register, message.content)
    if is_task_register:
        register_task(message)


message = "【dddd(あいうえお)[http://<>]】11/11 11:11"
register_task(message)
