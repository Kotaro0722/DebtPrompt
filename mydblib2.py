import mysql.connector as mydb
import pandas as pd
import sys
import config


def my_update(db, sql_string):
    try:
        dbcon = mydb.connect(
            host="localhost",
            user=config.USER,
            password=config.PASSWORD,
            database=db
        )
        cursor = dbcon.cursor(dictionary=True)
    except mydb.Error as e:
        print(f"DBコネクションでエラー発生\n{e}")
        sys.exit()

    try:
        cursor.execute(sql_string)
        dbcon.commit()
    except mydb.Error as e:
        print(f"クエリ実行でエラー発生\n{e}")
        print(f"入力されたSQLは\n{sql_string}")
        sys.exit()
