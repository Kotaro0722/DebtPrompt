# テストケース一覧: `main.on_message`

## 対象関数

```python
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    is_all_debt=re.fullmatch(f"<@{client.user.id}>",message.content)

    if is_all_debt:
        await show_all_credit(message.author.id,message)
    elif re.fullmatch(fr"<@{client.user.id}>\s*(?:<@(\d+)>\s*)+",message.content):
        ids=re.findall(r"<@(\d+)>",message.content)
        ids.remove(str(client.user.id))
        channel_member= get_member_list(message)
        is_only_user=all(int(id) in channel_member for id in ids)
        if is_only_user:
            for id in ids:
                await show_one_credit(message.author.id, id, message)
    elif re.fullmatch(fr"<@{client.user.id}>\s*scroll",message.content):
        register_channel = client.get_channel(int(register_channel_id))
        await scroll_message(register_channel)
    elif re.fullmatch(fr"<@{client.user.id}>\s*delete",message.content):
        register_channel = client.get_channel(int(register_channel_id))
        await delete_circle(register_channel)
    elif re.search(rf"<@{client.user.id}>",message.content):
        await message.add_reaction("🤖")
        await message.add_reaction("❌")
    elif re.fullmatch(await get_register_pattern(message), message.content):
        id=message.id
        creditor=message.author.id
        debtor,amount=re.match(r"<@(\d+)>\s+(\d+)円",message.content).groups()
        register_DB(id, creditor, debtor, amount, 0)
        await message.add_reaction("⭕")
```

- ユーザーからのメッセージを内容によって振り分ける、`if/elif`チェーンによる分岐処理
- `elif`チェーンなので、各メッセージは**必ずどれか1つのケースにしか該当しない**（MECEが構造的に保証されている）

## MECEの切り口（`if/elif`の各分岐＋どれにも該当しないケース）

| # | 条件 | 呼ばれる処理 |
|---|---|---|
| 0 | 送信者がBot自身 | 何もしない（早期return） |
| 1 | `<@bot>`のみ | `show_all_credit` |
| 2 | `<@bot> <@debtor1> <@debtor2>...` | チャンネルメンバー全員に該当する場合のみ、各debtorに`show_one_credit` |
| 3 | `<@bot> scroll` | `scroll_message` |
| 4 | `<@bot> delete` | `delete_circle` |
| 5 | botへのメンションを含むが1〜4に一致しない | 🤖❌ リアクションを付ける |
| 6 | 借金登録パターンに一致（例：`<@111> 500円 詳細`） | `register_DB` + ⭕リアクション |
| 7 | 上記のどれにも一致しない | 何もしない |

## テストケース表

| No | 分類 | ケース内容 | 入力例 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | #0 | 送信者がBot自身のメッセージ | `message.author == client.user` | 何も処理されない | - | 未実装 |
| 2 | #1 | `<@bot>`のみのメッセージ | `"<@BOT_ID>"` | `show_all_credit(message.author.id, message)`が呼ばれる | - | 未実装 |
| 3 | #2 | `<@bot> <@debtor>`で、debtorがチャンネルメンバーに含まれる | `"<@BOT_ID> <@111>"` | `show_one_credit`が呼ばれる | - | 未実装 |
| 4 | #2 | `<@bot> <@debtor>`で、debtorがチャンネルメンバーに含まれない | `"<@BOT_ID> <@999>"` | `show_one_credit`は呼ばれない | - | 未実装 |
| 5 | #2 | `<@bot> <@debtor1> <@debtor2>`で複数debtorを指定 | `"<@BOT_ID> <@111> <@222>"` | debtorごとに`show_one_credit`が呼ばれる | - | 未実装 |
| 6 | #3 | `<@bot> scroll` | `"<@BOT_ID> scroll"` | `scroll_message`が呼ばれる | - | 未実装 |
| 7 | #4 | `<@bot> delete` | `"<@BOT_ID> delete"` | `delete_circle`が呼ばれる | - | 未実装 |
| 8 | #5 | botへのメンションを含むが認識できないコマンド | `"<@BOT_ID> foo"` | 🤖と❌のリアクションが付く | - | 未実装 |
| 9 | #6 | 借金登録パターンに一致するメッセージ | `"<@111> 500円 詳細"` | `register_DB(id, creditor, debtor, amount, 0)`が呼ばれ、⭕が付く | - | 未実装 |
| 10 | #7 | botへのメンションも登録パターンも無いメッセージ | `"こんにちは"` | 何も処理されない | - | 未実装 |

## スコープ外 / 備考

- **既知の実装上の懸念（要確認）**：`#2`の分岐内で `channel_member= get_member_list(message)` としているが、`get_member_list`は`async def`であるにもかかわらず`await`されていない。これは`await`漏れであれば`channel_member`は`list`ではなく`coroutine`オブジェクトになり、続く`int(id) in channel_member`が`TypeError`になる可能性がある。テスト作成時に実際の挙動を確認し、バグであれば別途修正を検討する
- `client.get_channel`は同期メソッド、`channel.fetch_message`等は非同期メソッドなので、モックの種類（`Mock`か`AsyncMock`か）を関数ごとに正しく選ぶ必要がある
