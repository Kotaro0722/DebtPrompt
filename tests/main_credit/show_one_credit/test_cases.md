# テストケース一覧: `main_credit.show_one_credit`

## 対象関数

```python
async def show_one_credit(creditor, debtor, message):
    sql_string = f"SELECT amount FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(sql_string)
    sum = data.sum(numeric_only=True)
    debtor_user=await client.fetch_user(debtor)
    message_send = await message.channel.send(f"{debtor_user.mention} {sum.iloc[-1]}円")

    sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={debtor} AND ispay=0;"
    data = my_select(sql_string)
    create_total(message_send.id, data)
```

- `show_all_credit` の「1人分だけ」版。ループが無く、常にメッセージ送信と `create_total` を1回だけ行う
- **注目点**：`show_all_credit` と異なり「該当データが0件」の場合の分岐が実装されていない。`data.sum(numeric_only=True)` は該当データが無いと空の `Series` を返し、続く `sum.iloc[-1]` が **`IndexError` になる**（意図した分岐ではなく、未考慮のエッジケース）

## MECEの切り口

- **A. 該当する未払い債権が1件以上ある**（正常に金額が集計されメッセージが送信される）
- **B. 該当する未払い債権が0件**（`sum.iloc[-1]` が `IndexError` を発生させる＝現状の実装上の欠陥）
- **C. 異常系**：依存先（`my_select`）自体が失敗する

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 該当する未払い債権が1件のとき | 1件分のデータ | 金額付きでメッセージが送信され、`create_total` が呼ばれる | - | 未実装 |
| 2 | A | 該当する未払い債権が複数件のとき | 複数件分のデータ | 合計された金額でメッセージが送信される | - | 未実装 |
| 3 | B | 該当する未払い債権が0件のとき | `my_select` が空のDataFrameを返す | `IndexError` が発生する（現状の実装の既知の欠陥として記録） | - | 未実装 |
| 4 | C | `my_select` が失敗した場合 | `my_select` が例外を発生 | `show_one_credit` は例外を握りつぶさず伝播する | - | 未実装 |

## スコープ外 / 備考

- No.3は「バグの再現テスト」であり、正常な仕様として期待している挙動ではない。将来 `show_one_credit` に0件時のガード（例：早期return）を追加する場合は、このテストの期待値を「メッセージが送信されず正常終了する」に更新する必要がある
- `client.fetch_user` は `AsyncMock` でモックする
