import MySQLdb

conn = MySQLdb.connect(
    host="localhost",
    user="root",
    password="kotaro0722",
    db="test_debt"
)

cursor = conn.cursor()

sql_create_table = "CREATE TABLE debt(id INT PRIMARY KEY,creditor VARCHAR(10),debtor VARCHAR(10),amount INT,ispay BOOLEAN)"
sql_show_table = "SELECT * FROM debt"
sql_insert_data = "INSERT INTO debt(id,creditor,debtor,amount,ispay) values(1,'kotaro','tomohisa','100',0)"
sql_alter_column1 = "ALTER TABLE debt MODIFY COLUMN id BIGINT"
sql_alter_column2 = "ALTER TABLE debt MODIFY COLUMN creditor BIGINT, MODIFY COLUMN debtor BIGINT"
sql_delete_data = "DELETE FROM debt WHERE id = 1;"

cursor.execute(sql_alter_column2)

for row in cursor:
    print(row)

# cursor.execute("CREATE DATABASE IF NOT EXISTS test_debt")

conn.commit()

cursor.close()
conn.close()
