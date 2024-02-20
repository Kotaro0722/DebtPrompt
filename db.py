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

sql_create_table = "CREATE TABLE debt(id BIGINT PRIMARY KEY,creditor BIGINT,debtor BIGINT,amount INT,ispay BOOLEAN)"
sql_show_table = "SELECT * FROM debt"
sql_show_table_detail = "SHOW COLUMNS FROM debt"
sql_insert_data = "INSERT INTO debt(id,creditor,debtor,amount,ispay) values(1,'kotaro','tomohisa',100,0)"
sql_alter_column1 = "ALTER TABLE debt MODIFY COLUMN id BIGINT"
sql_alter_column2 = "ALTER TABLE debt MODIFY COLUMN creditor BIGINT, MODIFY COLUMN debtor BIGINT"
sql_delete_data = "DELETE FROM debt WHERE id = 1;"
sql_select_data = "SELECT debtor,amount,ispay FROM debt WHERE ispay=0 AND creditor=960825958208765973"
sql_delete_table = "DROP TABLE debt"
sql_delete_table_2 = "DROP TABLE sum_1209423440495509504"

cursor.execute(sql_create_table)

for row in cursor:
    print(row)

# cursor.execute("CREATE DATABASE IF NOT EXISTS test_debt")

conn.commit()

cursor.close()
conn.close()
