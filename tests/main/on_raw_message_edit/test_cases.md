# テストケース一覧: `main.on_raw_message_edit`

## 対象関数

```python
@client.event
async def on_raw_message_edit(payload:discord.RawMessageUpdateEvent):
    author=payload.data["author"]["id"]
    if author==client.user:
        return

    guild=await client.fetch_guild(payload.guild_id)
    channel=await guild.fetch_channel(payload.channel_id)
    message=await channel.fetch_message(payload.data["id"])

    message.content=message.content

    pattern_is_update = await get_register_pattern(message,guild)
    is_update=re.fullmatch(pattern_is_update,message.content)
    if is_update:
        id=message.id
        creditor=author
        debtor,amount=re.match(r"<@(\d+)>\s+(\d+)円",message.content).groups()
        ispay=any(reaction.emoji=="✅" for reaction in message.reactions)
        update_DB(id,creditor,debtor,amount,ispay)
        await message.add_reaction("⭕")
    else:
        await message.remove_reaction("⭕",client.user)
```

- メッセージ編集イベントを受け、編集後の内容が借金登録パターンに一致するかで「DB更新」か「⭕取り消し」に分岐する

## MECEの切り口

- **A. 編集者がBot自身**（早期return）
- **B. 編集後の内容が登録パターンに一致する**（`update_DB`が呼ばれ⭕が付く）
- **C. 編集後の内容が登録パターンに一致しない**（⭕リアクションが外される）
- **D. 異常系**：`update_DB`が失敗する

## テストケース表

| No | 分類 | ケース内容 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|----------------|----------------|------|
| 1 | A | 編集者がBot自身のとき | 何も処理されない（早期return） | - | 未実装 |
| 2 | B | 編集後の内容が登録パターンに一致するとき | `update_DB`が本文から抽出した`debtor`/`amount`/`ispay`で呼ばれ、⭕が付く | - | 未実装 |
| 3 | B | 編集後のメッセージに✅リアクションが付いている | `ispay=True`で`update_DB`が呼ばれる | - | 未実装 |
| 4 | B | 編集後のメッセージに✅リアクションが付いていない | `ispay=False`で`update_DB`が呼ばれる | - | 未実装 |
| 5 | C | 編集後の内容が登録パターンに一致しないとき | `update_DB`は呼ばれず、⭕リアクションが外される | - | 未実装 |
| 6 | D | `update_DB`が失敗した場合 | 例外が伝播し、⭕リアクションは付かない | - | 未実装 |

## スコープ外 / 備考

- **既知の実装上の懸念（要確認）**：`author=payload.data["author"]["id"]`は生のID（intまたはstr）であり、`client.user`は`discord.ClientUser`オブジェクトである。`author==client.user`という比較は型が異なるため、意図している「Bot自身による編集はスキップする」が実際には機能していない（常に`False`になる）可能性がある。テスト作成時に実際の挙動を確認し、バグであれば別途修正を検討する
- `payload.data`は生のREST APIレスポンス相当の`dict`なので、モックする際は実際のキー構造（`{"author": {"id": ...}, "id": ...}`）に合わせる
