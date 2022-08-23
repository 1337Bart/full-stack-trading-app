import sqlite3, config

connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_price (
        timestamp NOT NULL,
        open NOT NULL,
        high NOT NULL,
        low NOT NULL,
        close NOT NULL,
        volume NOT NULL,
        trade_count NOT NULL, 
        vwap NOT NULL,
        symbol NOT NULL,
        stock_id NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock(id)
    )
""")


connection.commit()