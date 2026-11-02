# テストケース一覧: `main_pay.cancel_one_pay_debt`

## 対象関数

```python
def cancel_one_pay_debt(message_id):
    sql_string = f"UPDATE {main_table} SET ispay=0 WHERE id={message_id}"
    my_update(sql_string)
```

- `pay_one_debt` の逆（`ispay` を0に戻す）で、構造は完全に同じ

## MECEの切り口

- **A. 正常系**：`my_update` が正常に完了する
- **B. 異常系**：`my_update` が失敗し、例外が発生する

## テストケース表

| No | 分類 | ケース内容 | 入力例 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A. 正常系 | 基本的な `message_id` でUPDATE文が正しく組み立てられる | `message_id=100` | `"UPDATE {main_table} SET ispay=0 WHERE id=100"` を引数に `my_update` が1回呼ばれる | - | 未実装 |
| 2 | B. 異常系 | `my_update` が失敗した場合、`cancel_one_pay_debt` は例外を握りつぶさず伝播する | `my_update` が例外を発生 | `cancel_one_pay_debt` の呼び出しが例外を発生させる | - | 未実装 |
