# テストケース一覧: `main_pay.pay_all_debt`

## 対象関数

```python
async def pay_all_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    for i in range(len(data)):
        pay_one_debt(data.at[i, "debt_id"])
        message = await channel.fetch_message(data.at[i, "debt_id"])
        await message.add_reaction("✅")
```

- 合計表示メッセージに紐づく個別の債権をすべて回収済みにする。`total` テーブルから明細を取得し、1件ずつ `pay_one_debt` を呼び、対応するDiscordメッセージに✅を付ける
- ループ回数が明細の件数に依存する

## MECEの切り口

- **A. 対象明細が0件**（ループが0回）
- **B. 対象明細が1件**（ループが1回）
- **C. 対象明細が複数件**（ループがN回）
- **D. 異常系**：`my_select` が失敗する
- **E. 異常系**：ループ中に `pay_one_debt`（内部で`my_update`）または `channel.fetch_message` が失敗する

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 対象明細が0件のとき | `my_select` が空のDataFrameを返す | `pay_one_debt`／`channel.fetch_message`／`add_reaction` は一度も呼ばれない | - | 未実装 |
| 2 | B | 対象明細が1件のとき | 1件分のデータ | `pay_one_debt` が1回呼ばれ、該当メッセージに✅が付く | - | 未実装 |
| 3 | C | 対象明細が複数件のとき | 3件分のデータ | 件数分繰り返され、各明細の `debt_id` に対して処理される | - | 未実装 |
| 4 | D | `my_select` が失敗した場合 | `my_select` が例外を発生 | 例外が伝播し、ループは実行されない | - | 未実装 |
| 5 | E | ループの途中で `pay_one_debt` が失敗した場合 | 2件目の呼び出しで例外を発生 | 例外が伝播し、3件目以降は処理されない | - | 未実装 |

## スコープ外 / 備考

- `channel.fetch_message` と `message.add_reaction` は `AsyncMock` でモックする
