# テストケース一覧: `main.on_raw_message_delete`

## 対象関数

```python
@client.event
async def on_raw_message_delete(payload:discord.RawMessageDeleteEvent):
    delete_DB(payload.message_id)
```

- メッセージ削除イベントを受け、そのまま`delete_DB`を呼ぶだけの薄いラッパー。分岐は無い

## MECEの切り口

- **A. 正常系**：`delete_DB`が正常に呼ばれる
- **B. 異常系**：`delete_DB`が失敗し、例外が発生する

## テストケース表

| No | 分類 | ケース内容 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|----------------|----------------|------|
| 1 | A | 通常のメッセージ削除イベントを受けたとき | `delete_DB(payload.message_id)`が1回呼ばれる | - | 未実装 |
| 2 | B | `delete_DB`が失敗した場合 | 例外が伝播する | - | 未実装 |
