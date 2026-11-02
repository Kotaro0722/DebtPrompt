# テストケース一覧: `main_credit.create_total`

## 対象関数

```python
def create_total(message_id, debt_ids):
    for debt_id in debt_ids["id"].tolist():
        sql_string = f"INSERT INTO total (message_id,debt_id) VALUES ({message_id},{debt_id})"
        my_update(sql_string)
```

- `debt_ids`（DataFrame）の `id` 列を1行ずつ取り出し、`total` テーブルへINSERTする
- ループ回数が `debt_ids` の行数に依存する

## MECEの切り口

- **A. `debt_ids` が0件**（ループが0回）
- **B. `debt_ids` が1件**（ループが1回）
- **C. `debt_ids` が複数件**（ループがN回）
- **D. 異常系**：ループの途中で `my_update` が失敗する

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | `debt_ids` が空のDataFrameのとき | `debt_ids["id"]` が空 | `my_update` は一度も呼ばれない | - | 未実装 |
| 2 | B | `debt_ids` が1件のとき | `id=[10]` | `my_update` が正しいSQLで1回呼ばれる | - | 未実装 |
| 3 | C | `debt_ids` が複数件のとき | `id=[10, 20, 30]` | 件数分（3回）`my_update` が呼ばれ、それぞれの `debt_id` がSQLに反映されている | - | 未実装 |
| 4 | D | ループの途中（例：2件目）で `my_update` が失敗した場合 | `my_update` の2回目の呼び出しで例外を発生させる | 例外が伝播し、3件目以降の `my_update` は呼ばれない（`call_count == 2` で停止） | - | 未実装 |

## スコープ外 / 備考

- `debt_ids` は `pandas.DataFrame` を渡す前提（`main_credit.py` 内の他関数は `my_select` の戻り値をそのまま渡している）
