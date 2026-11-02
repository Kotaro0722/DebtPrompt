from unittest.mock import patch

import pytest

import main_db
from main_db import register_DB


# No.1 正常系:基本的な値でSQLが正しく組み立てられる
@patch("main_db.my_update")
def test_success(mock_my_update):
    register_DB(id=100, creditor=111, debtor=222, amount=5000, ispay=0)

    mock_my_update.assert_called_once_with(
        f"INSERT INTO {main_db.main_table}(id,creditor,debtor,amount,ispay) "
        "values(100,'111','222','5000',0)"
    )


# No.2, No.3 正常系:ispayの値(0/1)がそのままSQLに埋め込まれる
@pytest.mark.parametrize("ispay", [0, 1])
@patch("main_db.my_update")
def test_ispay_is_passed_through(mock_my_update, ispay):
    register_DB(id=200, creditor=1, debtor=2, amount=300, ispay=ispay)

    sql = mock_my_update.call_args[0][0]
    assert sql.endswith(f",{ispay})")


# No.4, No.5 正常系:amountが負の値(返済扱い)や0の境界値でも正しくSQLに埋め込まれる
@pytest.mark.parametrize("amount", [-500, 0])
@patch("main_db.my_update")
def test_amount_boundary_values_are_passed_through(mock_my_update, amount):
    register_DB(id=300, creditor=1, debtor=2, amount=amount, ispay=0)

    sql = mock_my_update.call_args[0][0]
    assert f"'{amount}'" in sql


# No.6 正常系:id/creditor/debtorがDiscordスノーフレーク相当の大きい整数でも正しく埋め込まれる
@patch("main_db.my_update")
def test_snowflake_sized_ids_are_passed_through(mock_my_update):
    snowflake_id = 123456789012345678

    register_DB(id=snowflake_id, creditor=snowflake_id, debtor=snowflake_id, amount=100, ispay=0)

    mock_my_update.assert_called_once_with(
        f"INSERT INTO {main_db.main_table}(id,creditor,debtor,amount,ispay) "
        f"values({snowflake_id},'{snowflake_id}','{snowflake_id}','100',0)"
    )


# No.7 正常系:creditor/debtorがstr型で渡されてもint型と同じSQLになる
@patch("main_db.my_update")
def test_creditor_debtor_str_and_int_produce_same_sql(mock_my_update):
    register_DB(id=400, creditor=111, debtor=222, amount=100, ispay=0)
    sql_from_int = mock_my_update.call_args[0][0]

    mock_my_update.reset_mock()
    register_DB(id=400, creditor="111", debtor="222", amount=100, ispay=0)
    sql_from_str = mock_my_update.call_args[0][0]

    assert sql_from_int == sql_from_str


# No.8 異常系:my_update(DB書き込み)が失敗した場合、register_DBは例外を握りつぶさずそのまま伝播させる
# (実際のmy_updateはDBエラー時にsys.exit()を呼ぶため、ここではSystemExitを模している)
@patch("main_db.my_update", side_effect=SystemExit(1))
def test_register_DB_propagates_error_from_my_update(mock_my_update):
    with pytest.raises(SystemExit):
        register_DB(id=100, creditor=111, debtor=222, amount=5000, ispay=0)
