# テストケース一覧: `main_message.get_member_list`

## 対象関数

```python
async def get_member_list(message,guild=None):
    members = message.guild.members if not guild else  [member async for member in guild.fetch_members()]
    memberList = [member.id for member in members if not member.bot]
    return memberList
```

- サーバーに存在するBot以外のメンバーIDのリストを返す
- `guild` 引数の有無で、メンバー取得元が切り替わる（`message.guild.members`のキャッシュ利用 or `guild.fetch_members()`の非同期取得）

## MECEの切り口

- **A. `guild` が未指定**（`message.guild.members` を使用）
- **B. `guild` を指定**（`guild.fetch_members()` を使用）

A・Bそれぞれの中で、メンバー構成のパターン（Botを含む／含まない、0人）による分岐は無い（常に同じフィルタ処理）ため、代表的な入力パターンで網羅する。

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | `guild` 未指定、Bot以外のメンバーのみのとき | `message.guild.members` に人間3人 | 3人分のIDがリストで返る | - | 未実装 |
| 2 | A | `guild` 未指定、Botが混在しているとき | `message.guild.members` に人間2人＋Bot1人 | Botを除いた2人分のIDのみ返る | - | 未実装 |
| 3 | A | `guild` 未指定、メンバーが0人のとき | `message.guild.members` が空 | 空リストが返る | - | 未実装 |
| 4 | B | `guild` を指定したとき | `guild.fetch_members()` が非同期イテレータでメンバーを返す | `message.guild.members` ではなく `guild.fetch_members()` の結果が使われる | - | 未実装 |
| 5 | B | `guild` 指定時にBotが混在しているとき | 人間2人＋Bot1人 | Botを除いた2人分のIDのみ返る | - | 未実装 |

## スコープ外 / 備考

- `guild.fetch_members()` は非同期イテレータ（`async for`）なので、モックには `unittest.mock.MagicMock` の `__aiter__`/`__anext__` を実装するか、テスト用の非同期ジェネレータを渡す
