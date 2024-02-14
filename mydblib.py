import MySQLdb
import pandas as pd
import sys


def my_select(db, sql_string):
    try:
        dbcon = MySQLdb.connect(
            host="localhost",
            user="root",
            password="kotaro0722",
            database=db
        )
        cursor = dbcon.cursor()
    except MySQLdb.Error as e:
        print(f"DBコネクションでエラー発生\n{e}")
        sys.exit()

    try:
        cursor.execute(sql_string)
        recset = cursor.fetchall()
        print(recset)
    except MySQLdb.Error as e:
        print(f"クエリ実行でエラー発生\n{e}")
        print(f"入力されたSQLは\n{sql_string}")
        sys.exit()

    return pd.DataFrame(recset)
