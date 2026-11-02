# テストケース一覧: `db.db_update.my_update`

## 対象関数

```python
def my_update( sql_string):
    try:
        dbcon = get_connection_pool().get_connection()
        cursor = dbcon.cursor(dictionary=True)
    except mydb.Error as e:
        print(f"DBコネクションでエラー発生\n{e}")
        sys.exit()

    try:
        cursor.execute(sql_string)
        dbcon.commit()
        cursor.close()
        dbcon.close()
    except mydb.Error as e:
        print(f"クエリ実行でエラー発生\n{e}")
        print(f"入力されたSQLは\n{sql_string}")
        sys.exit()
```

- `main_db.py`/`main_credit.py`/`main_pay.py`/`main.py`から呼ばれる、DB更新系(INSERT/UPDATE/DELETE)の唯一の実行経路
- 「接続取得」と「クエリ実行」の2段階の`try`があり、それぞれ`mysql.connector.Error`（`mydb.Error`）のみを捕捉して`sys.exit()`する

## MECEの切り口

- **A. 正常系**：接続取得・クエリ実行ともに成功する
- **B. 異常系**：接続取得(`get_connection_pool().get_connection()`)が`mydb.Error`を発生させる
- **C. 異常系**：クエリ実行(`cursor.execute`)が`mydb.Error`を発生させる
- **D. スコープ外**：`mydb.Error`以外の例外（`except`で捕捉されないため、そのまま伝播する）

A・B・Cは「どの段階で失敗するか」で完全に分割される（両方成功／接続で失敗／実行で失敗、の3択で全ケースを尽くす）。

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 接続・クエリ実行ともに成功する | 正常なSQL文字列 | `cursor.execute`にSQLが渡り、`dbcon.commit()`・`cursor.close()`・`dbcon.close()`が呼ばれる | - | 未実装 |
| 2 | B | 接続取得時に`mydb.Error`が発生する | `get_connection_pool().get_connection()`が`mydb.Error`を発生 | `sys.exit()`が呼ばれる（`SystemExit`が発生する） | - | 未実装 |
| 3 | C | クエリ実行時に`mydb.Error`が発生する | `cursor.execute`が`mydb.Error`を発生 | `sys.exit()`が呼ばれる（`dbcon.commit()`は呼ばれない） | - | 未実装 |

## スコープ外 / 備考

- `mydb.Error`以外の例外（例：`TypeError`）は`except`で捕捉されずそのまま呼び出し元に伝播する。これは現在の実装が意図的に`mydb.Error`のみを対象にしているためで、バグではなく仕様として記録し、テスト対象外とする
- 接続プールの生成自体は`db_pool.get_connection_pool`側の責務なので、`my_update`のテストでは`get_connection_pool`をモックし、`.get_connection()`の戻り値（コネクション・カーソルのモック）を制御する
