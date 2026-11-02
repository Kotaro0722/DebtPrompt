# テストケース一覧: `main.on_raw_reaction_remove`

## 対象関数

```python
@client.event
async def on_raw_reaction_remove(payload):
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.member

    if user == client.user:
        return

    if message.author.id != payload.user_id and message.author.id != client.user.id:
        return

    if payload.emoji.name != "✅":
        return

    register_channel = client.get_channel(int(register_channel_id))
    if message.author.id == client.user.id:
        await cancel_all_pay_debt(message.id, register_channel)
    else:
        cancel_one_pay_debt(message.id)
```

- `on_raw_reaction_add`の✅部分に対応する「リアクション取り消し」版。✅以外は早期returnで無視する（❔に相当する処理は無い）

## MECEの切り口

- **A. リアクションを外したのがBot自身**（早期return）
- **B. メッセージの投稿者が操作者本人でもBotでもない**（早期return）
- **C. 外されたリアクションが✅以外**（早期return）
- **D. ✅が外され、対象がBotの合計表示メッセージ**（`cancel_all_pay_debt`）
- **E. ✅が外され、対象が借金登録メッセージ**（`cancel_one_pay_debt`）

A〜Eの5つの早期return／分岐で、起こりうる全パターンを尽くしている。

## テストケース表

| No | 分類 | ケース内容 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|----------------|----------------|------|
| 1 | A | リアクションを外したのがBot自身のとき | 何も処理されない（早期return） | - | 未実装 |
| 2 | B | メッセージの投稿者が操作者本人でもBotでもないとき | 何も処理されない（早期return） | - | 未実装 |
| 3 | C | 外されたリアクションが✅以外（例：❔）のとき | 何も処理されない（早期return） | - | 未実装 |
| 4 | D | Botの合計表示メッセージから✅が外されたとき | `cancel_all_pay_debt(message.id, register_channel)`が呼ばれる | - | 未実装 |
| 5 | E | 借金登録メッセージ（投稿者が操作者自身）から✅が外されたとき | `cancel_one_pay_debt(message.id)`が呼ばれる | - | 未実装 |
| 6 | 異常系 | `cancel_all_pay_debt`/`cancel_one_pay_debt`が失敗する場合 | 例外が伝播する | - | 未実装 |

## スコープ外 / 備考

- `on_raw_reaction_add`と異なり、`user = payload.member`（`discord.Member`オブジェクト）を`client.user`（`discord.ClientUser`）と比較している。オブジェクト同士の比較なので`on_raw_reaction_add`の`payload.user_id`（生のint）との比較とは事情が異なる可能性があるが、discord.pyの実際の等価判定仕様に依存するため、テスト作成時に実際の挙動を確認すること
- ❔（詳細確認）に対応する処理は無い（`on_raw_reaction_add`側にしか存在しない）
