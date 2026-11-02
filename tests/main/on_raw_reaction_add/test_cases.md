# テストケース一覧: `main.on_raw_reaction_add`

## 対象関数

```python
@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    guild=await client.fetch_guild(payload.guild_id)
    txt_channel = client.get_channel(payload.channel_id)
    message = await txt_channel.fetch_message(payload.message_id)
    user = payload.user_id

    if user == client.user:
        return

    if message.author.id != payload.user_id and message.author.id != client.user.id:
        return

    if payload.emoji.name == "✅":
        if list(filter(lambda rea: rea.emoji == "✅", message.reactions))[0].me:
            await message.remove_reaction("✅", client.user)
            return

        register_channel = client.get_channel(int(register_channel_id))
        if message.author.id == client.user.id:
            await pay_all_debt(message.id, register_channel)
        else:
            pay_one_debt(message.id)

    if payload.emoji.name == "❔" and client.user.id == message.author.id:
        debtor=await guild.fetch_member(re.match(r"<@(\d+)>",message.content).group(1))
        await show_detail(message,debtor, txt_channel,payload)
```

- リアクション追加イベントを受け、✅（返済）または❔（詳細確認）のリアクションに応じて処理を振り分ける
- `if`が2つ続く構造で、✅用の`if`と❔用の`if`は独立している（両方に該当することは無い：`emoji.name`は1つのリアクションイベントにつき1種類のため）

## MECEの切り口

- **A. リアクションしたユーザーがBot自身**（早期return）
- **B. リアクションされたメッセージが「操作者自身の投稿」でも「Botの投稿」でもない**（早期return）
- **C. ✅リアクション、かつすでにBot自身の✅が付いている**（二重防止のため取り消してreturn）
- **D. ✅リアクション、対象がBotの合計表示メッセージ**（`pay_all_debt`）
- **E. ✅リアクション、対象が借金登録メッセージ**（`pay_one_debt`）
- **F. ❔リアクション、対象がBotの合計表示メッセージ**（`show_detail`）
- **G. ❔リアクション、条件に一致しない**（何もしない）

## テストケース表

| No | 分類 | ケース内容 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|----------------|----------------|------|
| 1 | A | リアクションしたのがBot自身のとき | 何も処理されない（早期return） | - | 未実装 |
| 2 | B | メッセージの投稿者が操作者本人でもBotでもないとき | 何も処理されない（早期return） | - | 未実装 |
| 3 | C | ✅を付けたが、既にBot自身の✅リアクションが付いているとき | Bot自身の✅が取り消され、以降の処理は行われない | - | 未実装 |
| 4 | D | Botの合計表示メッセージに✅が付いたとき | `pay_all_debt(message.id, register_channel)`が呼ばれる | - | 未実装 |
| 5 | E | 借金登録メッセージ（投稿者が操作者自身）に✅が付いたとき | `pay_one_debt(message.id)`が呼ばれる | - | 未実装 |
| 6 | F | Botの合計表示メッセージに❔が付いたとき | メッセージ本文からdebtorを特定し`show_detail`が呼ばれる | - | 未実装 |
| 7 | G | ❔が付いたが、メッセージの投稿者がBotでないとき | `show_detail`は呼ばれない | - | 未実装 |
| 8 | 異常系 | `pay_all_debt`/`pay_one_debt`/`show_detail`が失敗する場合 | 例外が伝播する | - | 未実装 |

## スコープ外 / 備考

- **既知の実装上の懸念（要確認）**：`user = payload.user_id`（生のint）を`client.user`（`discord.ClientUser`オブジェクト）と比較している。型が異なるため、`on_raw_message_edit`と同様に「Bot自身のリアクションはスキップする」が意図通り機能していない可能性がある
- ✅と❔の2つの`if`は独立しているため、テストでは「✅のケース」と「❔のケース」を明確に分けて`payload.emoji.name`を設定する
