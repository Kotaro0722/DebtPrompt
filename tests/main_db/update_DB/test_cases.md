# テストケース一覧: `main_db.update_DB`

## 対象関数

```python
def update_DB(id,creditor,debtor,amount,ispay):
    sql_update_data=f"INSERT INTO {main_table} (id,creditor,debtor,amount,ispay) VALUES ({id},'{creditor}','{debtor}',{amount},{ispay}) ON DUPLICATE KEY UPDATE debtor=VALUES(debtor), amount=VALUES(amount), ispay=VALUES(ispay);"
    my_update(sql_update_data)
```

- `id` が既存であれば更新、無ければ新規登録するUPSERT文(`ON DUPLICATE KEY UPDATE`)を組み立て、`my_update` を1回呼び出すだけの関数
- `register_DB` と似た形だが、`amount`/`ispay` はクォートせず数値のまま埋め込まれる点が異なる（`register_DB` は `amount` を `'...'` で囲む）

## MECEの切り口

`register_DB` と同様に分岐が無いため、結果は以下の2つで完全に分割できる。

- **A. 正常系**：`my_update` が正常に完了する（内部は「引数の値パターン」で網羅性を確保）
- **B. 異常系**：`my_update` が失敗し、例外が発生する

## テストケース表

| No | 分類 | ケース内容 | 入力例 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A. 正常系 | 基本的な値で `ON DUPLICATE KEY UPDATE` を含むSQLが正しく組み立てられる | `id=100, creditor=111, debtor=222, amount=5000, ispay=0` | 期待通りのSQL文を引数に `my_update` が1回呼ばれる | - | 未実装 |
| 2 | A. 正常系 | `ispay=0`/`ispay=1` が正しくSQLに反映される | `ispay=0`, `ispay=1` | SQLの `VALUES(...,ispay)` 部分に値がそのまま反映される | - | 未実装 |
| 3 | A. 正常系 | `amount` が負の値（返済扱い）や0の境界値でも正しく埋め込まれる | `amount=-500`, `amount=0` | SQLに `-500`/`0` がクォート無しで含まれる | - | 未実装 |
| 4 | A. 正常系 | `amount`/`ispay` がクォート無しで埋め込まれることの確認（`register_DB` との差異） | `amount=5000` | SQLに `'5000'` ではなく `5000`（クォート無し）が含まれる | - | 未実装 |
| 5 | B. 異常系 | `my_update` が失敗した場合、`update_DB` は例外を握りつぶさず伝播する | `my_update` が例外を発生 | `update_DB` の呼び出しが例外を発生させる | - | 未実装 |

## スコープ外

- `register_DB` と同様、引数の妥当性チェックが無いため、`None` 等の不正な入力による挙動は対象外（バリデーション欠如の問題であり、`update_DB` 自身の異常系ではない）
