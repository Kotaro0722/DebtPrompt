import sqlite3

dbname = 'DebtPrompt.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

createTable="""CREATE TABLE IF NOT EXISTS debt
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        debtor TEXT,
        creditor TEXT,
        amount INTEGER,
        detail TEXT
    )
    """
addColumn="ALTER TABLE debt ADD COLUMN isRepay INTEGER"

deleteTable="""DROP TABLE debt"""

insert="""INSERT INTO debt(debtor,creditor,amount,detail,isRepay) VALUES(:debtor,:creditor,:amount,:detail,:isRepay)"""
insertList={
    "debtor":"kotaro",
    "creditor":"tomohisa",
    "amount":400,
    "detail":"昼飯",
    "isRepay":0
}
    
select="SELECT creditor,amount,detail,isRepay FROM debt WHERE creditor=(:creditor)"
selectList={"creditor":"tanami"}

update="UPDATE debt SET creditor='tanami' WHERE id=7"

delete ="DELETE FROM debt"

cur.execute(select,selectList)
data=cur.fetchall()
print(data)
conn.commit()
cur.close()
conn.close()

# cur.execute('CREATE TABLE debt(id INTEGER PRIMARY KEY AUTOINCREMENT,debtor STRING,creditor STRING,amount INTEGER,detail STRING)')