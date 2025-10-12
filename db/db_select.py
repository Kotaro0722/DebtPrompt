import mysql.connector as mydb
from db.db_pool import connection_pool
import pandas as pd
import sys


def my_select(sql_string):
    try:
        dbcon=connection_pool.get_connection()
        cursor = dbcon.cursor(dictionary=True)
    except mydb.Error as e:
        print(f"DBコネクションでエラー発生\n{e}")
        sys.exit()

    try:
        cursor.execute(sql_string)
        recset = cursor.fetchall()
        cursor.close()
        dbcon.close()
        return pd.DataFrame(recset)
    except mydb.Error as e:
        print(f"クエリ実行でエラー発生\n{e}")
        print(f"入力されたSQLは\n{sql_string}")
        sys.exit()


