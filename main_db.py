import config
from db.db_update import my_update


main_table = config.MAIN_TABLE

# DBへ登録する
def register_DB(id, creditor, debtor, amount, ispay):
    sql_insert_data = f"INSERT INTO {main_table}(id,creditor,debtor,amount,ispay) values({id},'{creditor}','{debtor}','{amount}',{ispay})"
    my_update(sql_insert_data)

# DBを更新する
def update_DB(id,creditor,debtor,amount,ispay):
    sql_update_data=f"INSERT INTO {main_table} (id,creditor,debtor,amount,ispay) VALUES ({id},'{creditor}','{debtor}',{amount},{ispay}) ON DUPLICATE KEY UPDATE debtor=VALUES(debtor), amount=VALUES(amount), ispay=VALUES(ispay);"
    my_update(sql_update_data)

# Dbから削除する
def delete_DB(id):
    sql_delete_data=f"DELETE FROM {main_table} WHERE id={id};"
    my_update(sql_delete_data)
