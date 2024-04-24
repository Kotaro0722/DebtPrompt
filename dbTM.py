import mysql.connector as mydb
import config

# print(config.HOST)

conn = mydb.connect(
    host=config.HOST,
    user=config.USER,
    password=config.PASSWORD,
    db=config.DBNAME
)

cursor = conn.cursor()

sql_create_table="CREATE TABLE taskManager(id BIGINT PRIMARY KEY,thread BIGINT,deadline DATE)"