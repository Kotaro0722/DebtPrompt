# テストケース一覧: `main_db.register_DB`

## 対象関数

```python
def register_DB(id, creditor, debtor, amount, ispay):
    sql_insert_data = f"INSERT INTO {main_table}(id,creditor,debtor,amount,ispay) values({id},'{creditor}','{debtor}','{amount}',{ispay})"
    my_update(sql_insert_data)
```

- 引数からINSERT文を組み立て、`my_update`(DB書き込み)を1回呼び出すだけの関数
- 分岐や引数の妥当性チェックは存在しない

## MECEの切り口

`register_DB` 自身に条件分岐が無く、必ず「SQLを組み立てて `my_update` を1回呼ぶ」という単一の処理しか行わないため、**関数の結果**は以下の2つで完全に分割できる（これが唯一の分岐点＝`my_update`が成功するか失敗するか）。

- **A. 正常系**：`my_update` が正常に完了する
- **B. 異常系**：`my_update` が失敗し、例外が発生する

A（正常系）の中身は分岐が無いため、結果は常に同じ（SQLが組み立てられ、呼ばれる）。ここでの網羅性は「**入力される引数の値のパターン**」で確保する。各引数の意味に基づき、同値分割・境界値分析で代表値を洗い出す。

| 引数 | 取りうる値の分類 |
|---|---|
| `id` / `creditor` / `debtor` | Discordのスノーフレーク ID（桁数の大きい整数）。型は `int` / `str` のどちらで渡されるかで埋め込み結果が変わりうる |
| `amount` | 正の値（借金の登録）／ 0 ／ 負の値（README.md記載の仕様：**返済**を表す） |
| `ispay` | `0`（未払い）／ `1`（支払済み）の2値のみ |

---

## テストケース表

| No | 分類 | ケース内容 | 入力例 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A. 正常系 | 基本的な値でSQLが正しく組み立てられる | `id=100, creditor=111, debtor=222, amount=5000, ispay=0` | 期待通りのINSERT文を引数に `my_update` が1回呼ばれる | `test_success` | 実装済み |
| 2 | A. 正常系 | `ispay=0`（未払い）が正しくSQLに反映される | `ispay=0` | SQLが `...,0)` で終わる | `test_ispay_is_passed_through[0]` | 実装済み |
| 3 | A. 正常系 | `ispay=1`（支払済み）が正しくSQLに反映される | `ispay=1` | SQLが `...,1)` で終わる | `test_ispay_is_passed_through[1]` | 実装済み |
| 4 | A. 正常系 | `amount` が負の値（返済扱い）でも正しくSQLに埋め込まれる | `amount=-500` | SQLに `'-500'` が含まれる | `test_amount_boundary_values_are_passed_through[-500]` | 実装済み |
| 5 | A. 正常系 | `amount=0` の境界値 | `amount=0` | SQLに `'0'` が含まれる | `test_amount_boundary_values_are_passed_through[0]` | 実装済み |
| 6 | A. 正常系 | `id`/`creditor`/`debtor` がDiscordスノーフレーク相当の大きい整数でも正しく埋め込まれる | `id=123456789012345678` | SQLにその値がそのまま文字列化されて含まれる | `test_snowflake_sized_ids_are_passed_through` | 実装済み |
| 7 | A. 正常系 | `creditor`/`debtor` が `str` 型で渡されても `int` 型と同じSQLになる | `creditor="111"` と `creditor=111` | 生成されるSQL文字列が一致する | `test_creditor_debtor_str_and_int_produce_same_sql` | 実装済み |
| 8 | B. 異常系 | `my_update` が失敗した場合、`register_DB` は例外を握りつぶさず呼び出し元に伝播する | `my_update` が `SystemExit` を発生 | `register_DB` の呼び出しが `SystemExit` を発生させる | `test_register_DB_propagates_error_from_my_update` | 実装済み |

---

## スコープ外（あえて対象にしていないケース）

| ケース | 扱い |
|---|---|
| `id`/`creditor`/`debtor`/`amount` に `None` や空文字などの不正な値を渡した場合 | `register_DB` は入力値の妥当性チェックを行わないため、不正な値でもそのままSQL文字列に埋め込んで `my_update` を呼び出す。これは「関数が異常終了する」ケースではなく「不正なSQLを組み立てて実行してしまう」ケースであり、`register_DB` の異常系ではなく**入力バリデーションの欠如**という別の問題。対応するなら関数側にバリデーションを追加した上でテストを書くべきであり、現状の実装のテストとしては対象外とする |

## 備考

- No.4〜7は「同値分割・境界値分析に基づく網羅候補」として実装済みです。`register_DB` は単純な文字列組み立てのみで分岐が無いため、実利益（バグを検出できる可能性）は限定的ですが、将来のリファクタリング時にSQLの組み立て内容が意図せず変わってしまった場合の回帰検知として機能します。
