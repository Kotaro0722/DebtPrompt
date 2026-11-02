# テストケース一覧: `db.db_pool.get_connection_pool`

## 対象関数

```python
_connection_pool = None

def get_connection_pool():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="discord_pool",
            pool_size=3,  # 同時接続上限
            pool_reset_session=True,
            **dbconfig
        )
    return _connection_pool
```

- モジュールレベルのグローバル変数`_connection_pool`を使った遅延初期化（シングルトン）
- `import`しただけではDBに接続しない設計（`db_pool.py`をimportしても`MySQLConnectionPool`は作られない）ようにするために導入した関数

## MECEの切り口

- **A. 初回呼び出し**（`_connection_pool is None`）：`MySQLConnectionPool`を新規生成する
- **B. 2回目以降の呼び出し**（`_connection_pool`が既にある）：新規生成せず、キャッシュされたインスタンスを返す

## テストケース表

| No | 分類 | ケース内容 | 入力/状態 | 期待される結果 | 対応するテスト | 状態 |
|----|------|-----------|--------|----------------|----------------|------|
| 1 | A | 初回呼び出しのとき | `_connection_pool = None` の状態から呼ぶ | `MySQLConnectionPool`が1回だけ生成され、その戻り値が返る | - | 未実装 |
| 2 | A | 生成時に`config`の値が正しく渡される | `config.HOST`等に任意の値を設定 | `MySQLConnectionPool`が`host`/`user`/`password`/`database`にその値を渡して呼ばれる | - | 未実装 |
| 3 | B | 同じ呼び出し内で2回`get_connection_pool()`を呼ぶ | 1回目呼び出し後、続けて2回目を呼ぶ | `MySQLConnectionPool`は1回しか生成されず（`call_count == 1`）、2回とも同じインスタンスが返る | - | 未実装 |
| 4 | - | `db_pool`モジュールをimportするだけでは`MySQLConnectionPool`が生成されないことの確認 | `import db.db_pool`のみ実行 | `MySQLConnectionPool`が呼ばれない（importの副作用対策の検証） | - | 未実装 |

## スコープ外 / 備考

- **テスト間の汚染に注意**：`_connection_pool`はモジュールレベルのグローバル変数であり、あるテストで一度生成されるとプロセス内で（`unittest.mock.patch`で戻せない限り）**残り続ける**。これは`register_DB`のテストで説明した「Mockはテストごとに作り直される」話とは異なり、`_connection_pool`自体は本物のモジュール変数なので、テストごとに `db.db_pool._connection_pool = None` にリセットする処理（`pytest`の`fixture`など）を用意しないと、テストの実行順序によって結果が変わる可能性がある
