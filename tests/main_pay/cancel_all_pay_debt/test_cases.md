# テストケース一覧: `main_pay.cancel_all_pay_debt`

## 対象関数

```python
async def cancel_all_pay_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    for i in range(len(data)):
        cancel_one_pay_debt(data.at[i, "debt_id"])
        message = await channel.fetch_message(data.at[i, "debt_id"])
        await message.remove_reaction("✅", client.user)
```

- `pay_all_debt` の逆で、明細ごとに `cancel_one_pay_debt` を呼び、対応するDiscordメッセージから✅を外す
- 構造は `pay_all_debt` と完全に対応している（`add_reaction`→`remove_reaction`、`pay_one_debt`→`cancel_one_pay_debt`）

## MECEの切り口

- **A. 対象明細が0件**（ループが0回）
- **B. 対象明細が1件**（ループが1回）
- **C. 対象明細が複数件**（ループがN回）
- **D. 異常系**：`my_select` が失敗する
- **E. 異常系**：ループ中に `cancel_one_pay_debt` または `channel.fetch_message` が失敗する

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 対象明細が0件のとき | `my_select` が空のDataFrameを返す | `cancel_one_pay_debt`／`channel.fetch_message`／`remove_reaction` は一度も呼ばれない | - | 未実装 |
| 2 | B | 対象明細が1件のとき | 1件分のデータ | `cancel_one_pay_debt` が1回呼ばれ、該当メッセージから✅が外れる | - | 未実装 |
| 3 | C | 対象明細が複数件のとき | 3件分のデータ | 件数分繰り返される | - | 未実装 |
| 4 | B/C | `remove_reaction` が `client.user` を引数に呼ばれている | 任意の明細データ | `message.remove_reaction("✅", client.user)` の形で呼ばれていることを確認 | - | 未実装 |
| 5 | D | `my_select` が失敗した場合 | `my_select` が例外を発生 | 例外が伝播し、ループは実行されない | - | 未実装 |
| 6 | E | ループの途中で `cancel_one_pay_debt` が失敗した場合 | 2件目の呼び出しで例外を発生 | 例外が伝播し、3件目以降は処理されない | - | 未実装 |

## スコープ外 / 備考

- `channel.fetch_message` と `message.remove_reaction` は `AsyncMock` でモックする
