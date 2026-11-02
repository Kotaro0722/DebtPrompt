# テストケース一覧: `main_message.parse_register_message`

## 対象関数

```python
def parse_register_message(content):
    debtor, amount = re.match(r"<@(\d+)>\s*(-?[0-9]+)円", content).groups()
    return debtor, int(amount)
```

- 借金登録メッセージ（例：`<@123> 500円 詳細`）から債務者IDと金額を取り出す
- 金額がマイナスのとき（例：`<@123> -500円`）は一部返済として扱い、負の整数を返す
- `get_register_pattern` で一致を確認したメッセージに対してのみ呼ばれる前提

## テストケース表

| No | 分類 | ケース内容 | 入力例 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | 正常系 | 正の金額 | `"<@123> 500円 詳細"` | `("123", 500)` | `test_positive_amount` | 実装済 |
| 2 | 正常系 | マイナスの金額（一部返済） | `"<@123> -500円 返済"` | `("123", -500)` | `test_negative_amount` | 実装済 |
| 3 | 正常系 | メンションと金額の間に空白が無い | `"<@123>-500円"` | `("123", -500)` | `test_without_space` | 実装済 |
| 4 | 正常系 | 詳細内の数字に影響されない | `"<@123> -500円 3月分"` | `("123", -500)` | `test_numbers_in_detail_are_ignored` | 実装済 |
| 5 | 正常系 | `get_register_pattern` に一致するメッセージは必ず解析できる | 正/負/空白なしの各メッセージ | 例外にならず値が返る | `test_consistent_with_register_pattern` | 実装済 |
