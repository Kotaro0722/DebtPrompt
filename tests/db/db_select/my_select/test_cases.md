# テストケース一覧: `db.db_select.my_select`

## 対象関数

```python
def my_select(sql_string):
    try:
        dbcon=get_connection_pool().get_connection()
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
```

- `my_update`とほぼ同じ構造だが、SELECT結果を`pandas.DataFrame`として返す点が異なる
- 「接続取得」と「クエリ実行」の2段階の`try`があり、それぞれ`mydb.Error`のみを捕捉して`sys.exit()`する

## MECEの切り口

- **A. 正常系**：接続取得・クエリ実行ともに成功し、結果がDataFrameとして返る
- **B. 異常系**：接続取得時に`mydb.Error`が発生する
- **C. 異常系**：クエリ実行時に`mydb.Error`が発生する
- **D. スコープ外**：`mydb.Error`以外の例外

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 接続・クエリ実行ともに成功し、レコードが取得できる | `cursor.fetchall()`が複数レコードを返す | 取得したレコードがそのまま`pandas.DataFrame`として返る | - | 未実装 |
| 2 | A | 該当レコードが0件のとき | `cursor.fetchall()`が空リストを返す | 空の`pandas.DataFrame`が返る（呼び出し側でのIndexError等の原因になるケース。関連: `show_one_credit`のテストケース） | - | 未実装 |
| 3 | B | 接続取得時に`mydb.Error`が発生する | `get_connection_pool().get_connection()`が`mydb.Error`を発生 | `sys.exit()`が呼ばれる | - | 未実装 |
| 4 | C | クエリ実行時に`mydb.Error`が発生する | `cursor.execute`が`mydb.Error`を発生 | `sys.exit()`が呼ばれる（DataFrameは返らない） | - | 未実装 |

## スコープ外 / 備考

- `mydb.Error`以外の例外は捕捉されずそのまま伝播する（`my_update`と同様の仕様）
- `cursor`のモックは`dictionary=True`で作られる前提（`fetchall()`が辞書のリストを返す）なので、モックの戻り値も辞書のリスト形式にする
