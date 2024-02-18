import mysql.connector as mydb
import config

# print(config.HOST)

conn = mydb.connect(
    host="viaduct.proxy.rlwy.net",
    user="root",
    password="5HAH5Db63Chf1eAGB5fBf-A2CH42Aecg",
    port=10029,
    db="railway"
)

cursor = conn.cursor()

sql_create_table = "CREATE TABLE debt(id BIGINT PRIMARY KEY,creditor BIGINT,debtor BIGINT,amount INT,ispay BOOLEAN)"
sql_show_table = "SELECT * FROM test"
sql_insert_data = "INSERT INTO test(id,creditor,debtor,amount,ispay) values(1,'kotaro','tomohisa',100,0)"
sql_alter_column1 = "ALTER TABLE test MODIFY COLUMN id BIGINT"
sql_alter_column2 = "ALTER TABLE test MODIFY COLUMN creditor BIGINT, MODIFY COLUMN debtor BIGINT"
sql_delete_data = "DELETE FROM test WHERE id = 1;"
sql_select_data = "SELECT debtor,amount,ispay FROM test WHERE ispay=0 AND creditor=960825958208765973"
sql_delete_table = "DROP TABLE test1"

cursor.execute(sql_create_table)

for row in cursor:
    print(row)

# cursor.execute("CREATE DATABASE IF NOT EXISTS test_debt")

conn.commit()

cursor.close()
conn.close()
