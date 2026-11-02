# テストケース一覧: `main_message.scroll_message`

## 対象関数

```python
async def scroll_message(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        pattern_for_register = await get_register_pattern(message)
        for_register = re.fullmatch(pattern_for_register, message.content)
        if not message.author.bot and for_register:
            is_register = False
            is_pay = 0
            for reaction in message.reactions:
                if reaction.emoji == "⭕" and reaction.me:
                    is_register = True
                if reaction.emoji == "✅":
                    is_pay = 1
            if not is_register:
                pattern_debtor_id = "[0-9]+"
                debtor = re.findall(pattern_debtor_id, message.content)[0]
                amount = re.findall(pattern_debtor_id, message.content)[1]
                main_db.register_DB(message.id, message.author.id,
                             debtor, amount, is_pay)
            await message.add_reaction("⭕")
```

- チャンネルの履歴を古い順に走査し、借金登録メッセージをDBに取り込んで⭕リアクションを付ける（重複取り込み防止のため既に⭕が付いているものはスキップ）
- 1メッセージあたりの分岐が多いため、**メッセージ単位の分類**で網羅する

## MECEの切り口

1メッセージに対して起こりうる分岐は、以下の条件の組み合わせで完全に分割できる。

- 送信者がBotか否か
- 登録パターンに一致するか否か
- 既に自分（Bot）の⭕リアクションが付いているか否か
- ✅リアクションが付いているか否か

| 送信者 | パターン一致 | ⭕済み | ✅あり | 結果 |
|---|---|---|---|---|
| Bot | - | - | - | 何もしない（スキップ、⭕も付けない） |
| Botでない | 不一致 | - | - | 何もしない（スキップ、⭕も付けない） |
| Botでない | 一致 | 済み | - | `register_DB`は呼ばれない。⭕は再度付けられる |
| Botでない | 一致 | 未 | 無し | `register_DB(ispay=0)`が呼ばれ、⭕が付く |
| Botでない | 一致 | 未 | 有り | `register_DB(ispay=1)`が呼ばれ、⭕が付く |

## テストケース表

| No | 分類 | ケース内容 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|----------------|----------------|------|
| 1 | 正常系 | Botのメッセージはスキップされる | `register_DB`も`add_reaction`も呼ばれない | - | 未実装 |
| 2 | 正常系 | 登録パターンに一致しないメッセージはスキップされる | `register_DB`も`add_reaction`も呼ばれない | - | 未実装 |
| 3 | 正常系 | パターンに一致し、⭕未・✅無しのメッセージ | `register_DB`が`ispay=0`で呼ばれ、⭕が付く | - | 未実装 |
| 4 | 正常系 | パターンに一致し、⭕未・✅有りのメッセージ | `register_DB`が`ispay=1`で呼ばれ、⭕が付く | - | 未実装 |
| 5 | 正常系 | パターンに一致するが、既に自分（Bot）の⭕が付いているメッセージ | `register_DB`は呼ばれないが、⭕は再度付けられる | - | 未実装 |
| 6 | 正常系 | 履歴に複数メッセージがある場合、`oldest_first=True`の順で全件処理される | 各メッセージが履歴の順序どおりに処理される | - | 未実装 |
| 7 | 正常系 | メッセージ本文から債務者IDと金額を正しく抽出できる | `<@111> 500円 詳細`から`debtor="111"`, `amount="500"`が抽出され`register_DB`に渡る | - | 未実装 |
| 8 | 異常系 | ループの途中で`register_DB`が失敗した場合 | 例外が伝播し、以降のメッセージは処理されない | - | 未実装 |

## スコープ外 / 備考

- `channel.history()` は非同期イテレータなので、テストでは非同期ジェネレータ（またはそれを模したモック）を用意する
- `main_message.py` は `import main_db` としているため（`from main_db import register_DB` ではない）、`@patch("main_db.register_DB")` で直接 `main_db` モジュールの属性をパッチすれば十分（呼び出し時に `main_db.register_DB` として毎回属性参照されるため、`main_message.main_db.register_DB` と書いても同じ効果になる）
