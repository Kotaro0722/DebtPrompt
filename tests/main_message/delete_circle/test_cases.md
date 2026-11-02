# テストケース一覧: `main_message.delete_circle`

## 対象関数

```python
async def delete_circle(channel: discord.Thread):
    async for message in channel.history(oldest_first=True, limit=None):
        try:
            await message.remove_reaction("⭕")
        except Exception as e:
            print(e)
```

- チャンネルの履歴を走査し、各メッセージから⭕リアクションを外す。1件ごとに`try/except`で失敗を握りつぶし（`print`のみ）、次のメッセージの処理を継続する

## MECEの切り口

- **A. 履歴が0件**
- **B. `remove_reaction`が成功するメッセージ**
- **C. `remove_reaction`が例外を発生させるメッセージ**（`except Exception`で握りつぶされ処理は継続する）
- **D. 履歴に複数メッセージがあり、成功／失敗が混在する**

Bと C はこの関数唯一の`try/except`により明確に分割され、かつ「例外が起きても処理を継続する」という特性上、後続メッセージの処理有無を別途検証する必要がある。

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 履歴が0件のとき | `channel.history()` が何も返さない | `remove_reaction` は一度も呼ばれない | - | 未実装 |
| 2 | B | `remove_reaction` が成功するメッセージ1件 | 例外なし | 例外なく処理が完了する | - | 未実装 |
| 3 | C | `remove_reaction` が例外を発生させるメッセージ1件 | `remove_reaction` が例外を発生 | 例外は`delete_circle`の外へ伝播せず、`print`されるだけで正常終了する | - | 未実装 |
| 4 | D | 1件目で例外が発生し、2件目は成功するメッセージが混在する履歴 | 1件目: 例外／2件目: 成功 | 1件目の例外に関わらず2件目の`remove_reaction`も呼ばれる（処理が継続する） | - | 未実装 |

## スコープ外 / 備考

- 実際の`discord.Message.remove_reaction`は`(emoji, member)`の2引数を要求するため、`remove_reaction("⭕")`という現在の呼び出し（`member`引数が無い）は本物のdiscord.py APIでは`TypeError`になる可能性がある。ただし`except Exception`で握りつぶされるため、実行結果としては「常にNo.3のケースに該当する」状態になっていると考えられる。この点はバグの可能性として記録するが、修正は本タスクの範囲外とする
