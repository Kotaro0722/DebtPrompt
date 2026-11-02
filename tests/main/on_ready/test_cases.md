# テストケース一覧: `main.on_ready`

## 対象関数

```python
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    debt_table_create_sql="""
        CREATE TABLE IF NOT EXISTS debt(...)"""
    my_update(debt_table_create_sql)
    total_table_create_sql="""
        CREATE TABLE IF NOT EXISTS total(...)"""
    my_update(total_table_create_sql)
```

- Bot起動時に呼ばれ、`debt`テーブルと`total`テーブルを`CREATE TABLE IF NOT EXISTS`で作成する
- 条件分岐は無く、常に2回`my_update`を呼ぶだけ

## MECEの切り口

- **A. 正常系**：2回の`my_update`呼び出しがともに成功する
- **B. 異常系**：1回目（`debt`テーブル作成）が失敗する
- **C. 異常系**：2回目（`total`テーブル作成）が失敗する

## テストケース表

| No | 分類 | ケース内容 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|----------------|----------------|------|
| 1 | A | 正常に呼び出されたとき | `my_update`が2回呼ばれ、1回目は`debt`テーブル、2回目は`total`テーブルのCREATE文が渡される | - | 未実装 |
| 2 | B | 1回目の`my_update`（`debt`テーブル作成）が失敗する | 例外が伝播し、2回目（`total`テーブル作成）の`my_update`は呼ばれない | - | 未実装 |
| 3 | C | 2回目の`my_update`（`total`テーブル作成）が失敗する | 1回目は正常に呼ばれた上で、2回目の例外が伝播する | - | 未実装 |

## スコープ外 / 備考

- `main.py`は`db.db_update.my_update`を直接`from db.db_update import my_update`でimportしているため、パッチ対象は`main.my_update`になる（`main_db.py`とは別に、`main.py`自身も`my_update`を直接使っている点に注意）
