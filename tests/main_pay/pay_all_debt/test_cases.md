# テストケース一覧: `main_pay.pay_all_debt`

## 対象関数

```python
async def pay_all_debt(message_id, channel):
    sql_string = f"SELECT * FROM total WHERE message_id={message_id}"
    data = my_select(sql_string)
    debt_ids = data["debt_id"].tolist() if len(data) else []
    # 先にDBを全て更新する(リアクション付与の失敗で残りの債権が未回収のまま残らないようにする)
    for debt_id in debt_ids:
        pay_one_debt(debt_id)
    for debt_id in debt_ids:
        await _change_check_reaction(channel, debt_id, add=True)
```

- 合計表示メッセージに紐づく個別の債権をすべて回収済みにする。`total` テーブルから明細を取得し、1件ずつ `pay_one_debt` を呼び、対応するDiscordメッセージに✅を付ける
- ループ回数が明細の件数に依存する

## MECEの切り口

- **A. 対象明細が0件**（ループが0回）
- **B. 対象明細が1件**（ループが1回）
- **C. 対象明細が複数件**（ループがN回）
- **D. 異常系**：`my_select` が失敗する
- **E. 異常系**：DB更新中に `pay_one_debt`（内部で`my_update`）が失敗する
- **F. 異常系**：登録メッセージの取得やリアクション変更が失敗する（DB更新は全件行い、失敗した分は飛ばして処理を続ける）

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 対象明細が0件のとき | `my_select` が空のDataFrameを返す | `pay_one_debt`／`channel.fetch_message`／`add_reaction` は一度も呼ばれない | - | 未実装 |
| 2 | B | 対象明細が1件のとき | 1件分のデータ | `pay_one_debt` が1回呼ばれ、該当メッセージに✅が付く | - | 未実装 |
| 3 | C | 対象明細が複数件のとき | 3件分のデータ | 件数分繰り返され、各明細の `debt_id` に対して処理される | - | 未実装 |
| 4 | D | `my_select` が失敗した場合 | `my_select` が例外を発生 | 例外が伝播し、ループは実行されない | - | 未実装 |
| 5 | E | DB更新の途中で `pay_one_debt` が失敗した場合 | 2件目の呼び出しで例外を発生 | 例外が伝播し、3件目以降のDB更新とリアクション変更は行われない | - | 未実装 |
| 6 | F | 一部の登録メッセージの取得に失敗した場合（別チャンネル・削除済み） | 1件目の `fetch_message` が `discord.NotFound` を発生 | 全件のDBが更新され、残りのメッセージは✅が付く | `test_continue_when_fetch_fails` | 実装済 |

## スコープ外 / 備考

- `channel.fetch_message` と `message.add_reaction` は `AsyncMock` でモックする
