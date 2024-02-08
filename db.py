import MySQLdb

conn = MySQLdb.connect(
    host="localhost",
    user="root",
    password="kotaro0722",
    db="practice1"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM SEVENTEEN WHERE ID=1")
for row in cursor:
    print(row)
# cursor.execute("CREATE DATABASE IF NOT EXISTS test_debt")

conn.commit()

cursor.close()
conn.close()
