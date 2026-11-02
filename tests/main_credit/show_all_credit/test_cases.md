# テストケース一覧: `main_credit.show_all_credit`

## 対象関数

```python
async def show_all_credit(creditor, message):
    sql_string = f"SELECT debtor,amount FROM {main_table} WHERE creditor={creditor} AND ispay=0"
    data = my_select(sql_string)
    sum = data.groupby("debtor").sum(numeric_only=True)
    for i in range(len(sum)):
        debtor_user = await client.fetch_user(sum[i:i+1].index[0])
        message_send = await message.channel.send(f"{debtor_user.mention}:{sum[i:i+1]['amount'].iloc[-1]}円")

        sql_string = f"SELECT id FROM {main_table} WHERE creditor={creditor} AND debtor={sum[i:i+1].index[0]} AND ispay=0;"
        data = my_select(sql_string)
        create_total(message_send.id, data)
```

- 指定した債権者の未払い債権を `my_select` で取得し、債務者ごとに合計してメッセージ送信、`create_total` で合計対象を記録する
- 依存先：`my_select`（DB取得）、`client.fetch_user`、`message.channel.send`、`create_total`
- 未払い債権の債務者が **何人いるか（0人／1人／複数人）** によって処理回数が変わるのが唯一の分岐点

## MECEの切り口

- **A. 未払い債権が0件**（該当する債務者がいない）
- **B. 未払い債権の債務者が1人**
- **C. 未払い債権の債務者が複数人**
- **D. 異常系**：依存先（`my_select`）が失敗する

A〜Cは「ループ回数が0回／1回／N回」というループ構造から導かれる、重複の無い完全な分割。

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 該当する未払い債権が0件のとき | `my_select` が空のDataFrameを返す | `client.fetch_user`／`message.channel.send`／`create_total` は一度も呼ばれない | - | 未実装 |
| 2 | B | 未払い債権の債務者が1人のとき | 債務者1人分のデータ | その債務者宛に1回メッセージが送信され、`create_total` が1回呼ばれる | - | 未実装 |
| 3 | C | 未払い債権の債務者が複数人のとき | 債務者2人分のデータ | 債務者ごとにメッセージが送信され、それぞれ `create_total` が呼ばれる（合計金額は債務者ごとに正しく集計される） | - | 未実装 |
| 4 | B/C | 送信メッセージの金額が、同一債務者の複数レコードの合計になっている | 同一債務者に対する複数件の債権データ | `groupby("debtor").sum()` の結果どおり合算された金額が表示される | - | 未実装 |
| 5 | D | `my_select`（1回目 or 2回目の呼び出し）が失敗した場合 | `my_select` が例外を発生 | `show_all_credit` は例外を握りつぶさず伝播する | - | 未実装 |

## スコープ外 / 備考

- `my_select` はDataFrameを返すため、テストでは `pandas.DataFrame` をモックの戻り値として用意する必要がある
- `client.fetch_user` はDiscord APIへの非同期呼び出しのため、実際のBot起動なしにテストするには `unittest.mock.AsyncMock` を使う（`Mock`は`await`できないため）
