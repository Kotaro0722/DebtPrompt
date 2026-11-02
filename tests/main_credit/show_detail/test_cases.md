# テストケース一覧: `main_credit.show_detail`

## 対象関数

```python
async def show_detail(message, debtor, channel, payload):
    sql_string = f"SELECT * FROM total WHERE message_id={message.id}"
    data = my_select(sql_string)

    for i in range(len(data)):
        await channel.send(f"[{debtor.display_name}:その{i+1}](<https://discord.com/channels/{payload.guild_id}/{register_channel_id}/{data.at[i,'debt_id']}>)")
```

- 合計表示メッセージ(`message`)に紐づく個別の債権明細を、`total` テーブルから取得して1件ずつ「その1」「その2」…とラベル付けして送信する
- ループ回数が `my_select` の取得結果の件数に依存する

## MECEの切り口

- **A. 明細データが0件**（ループが0回）
- **B. 明細データが1件**（ループが1回、「その1」のみ）
- **C. 明細データが複数件**（ループがN回、「その1」「その2」…と連番）
- **D. 異常系**：`my_select` が失敗する

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 該当する明細データが0件のとき | `my_select` が空のDataFrameを返す | `channel.send` は一度も呼ばれない | - | 未実装 |
| 2 | B | 該当する明細データが1件のとき | 1件分のデータ | 「その1」というラベルでメッセージが1回送信される | - | 未実装 |
| 3 | C | 該当する明細データが複数件のとき | 3件分のデータ | 「その1」「その2」「その3」の順でメッセージが送信される | - | 未実装 |
| 4 | B/C | リンクのURLが `payload.guild_id` と各行の `debt_id` を使って正しく組み立てられている | 任意の `guild_id`/`debt_id` | 送信メッセージ内のURLに、その値が正しく反映されている | - | 未実装 |
| 5 | D | `my_select` が失敗した場合 | `my_select` が例外を発生 | `show_detail` は例外を握りつぶさず伝播する | - | 未実装 |

## スコープ外 / 備考

- `debtor.display_name` は `discord.Member` の属性なので、テストでは `Mock(display_name="...")` のような簡易オブジェクトで代替する
