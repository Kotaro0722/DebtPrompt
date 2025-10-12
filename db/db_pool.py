import mysql.connector.pooling
import config

dbconfig = {
    "host": config.HOST,
    "user": config.USER,
    "password": config.PASSWORD,
    "database": config.DBNAME
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="discord_pool",
    pool_size=3,  # 同時接続上限
    pool_reset_session=True,
    **dbconfig
)