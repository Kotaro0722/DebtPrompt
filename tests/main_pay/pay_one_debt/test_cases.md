# テストケース一覧: `main_pay.pay_one_debt`

## 対象関数

```python
def pay_one_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=1 WHERE id={message_id}"
    my_update(sql_string)
```

- `message_id` を条件にUPDATE文を組み立て、`my_update` を1回呼び出すだけの関数（`delete_DB` と同じ構造）

## MECEの切り口

- **A. 正常系**：`my_update` が正常に完了する
- **B. 異常系**：`my_update` が失敗し、例外が発生する

## テストケース表

| No | 分類 | ケース内容 | 入力例 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A. 正常系 | 基本的な `message_id` でUPDATE文が正しく組み立てられる | `message_id=100` | `"UPDATE {main_table} SET ispay=1 WHERE id=100"` を引数に `my_update` が1回呼ばれる | - | 未実装 |
| 2 | B. 異常系 | `my_update` が失敗した場合、`pay_one_debt` は例外を握りつぶさず伝播する | `my_update` が例外を発生 | `pay_one_debt` の呼び出しが例外を発生させる | - | 未実装 |
