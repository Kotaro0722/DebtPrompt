import mysql.connector.pooling
import config

dbconfig = {
    "host": config.HOST,
    "user": config.USER,
    "password": config.PASSWORD,
    "database": config.DBNAME
}

_connection_pool = None

# 実際にクエリを実行するまで接続プールを作らない(importするだけでDBに接続してしまうのを防ぐ)
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