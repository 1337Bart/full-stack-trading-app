import sqlite3, config
import alpaca_trade_api as tradeapi
from alpaca_trade_api import REST, TimeFrame
import pandas as pd
from sqlalchemy import create_engine

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)
engine = create_engine('sqlite:///C:/Users/Bruker/Desktop/app/app.db', echo=False)

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

count = 0
for row in rows:
    symbol = row['symbol']
    barsets = api.get_bars(symbol, TimeFrame.Day, "2021-01-01", adjustment='raw').df
    df = barsets
    df['symbol'] = symbol
    df['stock_id'] = row['id']
    df.to_sql('stock_price', con=engine, if_exists='append')
    print(f'processing {symbol}')
    #NEW
    count += 1
    print(f"Count: {count} out of {len(rows)}")
       
connection.commit()

#Errors:
#requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://data.alpaca.markets/v2/stocks/LTC/BTC/bars?timeframe=1Day&adjustment=raw&start=2021-01-01
#alpaca_trade_api.rest.APIError: endpoint not found

#Appears to be a problem with CRYPTOs only, as all the stocks are fine. Need to figure out a way to create another loop for crypto and add it as separate DB
#Alpaca: 403 - Forbidden Authentication headers are missing or invalid.



#old code
# symbols = []
# for row in rows:
#     symbol = row['symbol']
#     symbols.append(symbol)

# chunk_size = 200
# for i in range (0, len(symbols), chunk_size):
#    symbol_chunk = symbols[i:i+chunk_size]
#    barsets = api.get_bars(symbol_chunk, TimeFrame.Day, "2021-01-01", adjustment='raw').df
#   for bar in barsets[symbol]:
        #     stock_id = stock_dict[symbol]
        #     cursor.execute("""
        #     INSERT INTO stock_price (stock_id, timestamp, open, high, low, close, volume, trade_count, vwap)
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        #     """, (stock_id, bar.t.date(), bar.open, bar.high, bar.l, bar.c, bar.v, bar.tc, bar.vwap)) 

        #it over DF rows: for row in barsets.T.iteritems()
        
#mine latest
# symbols = [row['symbol'] for row in rows]
#stock_dict = {}
#temporary fix to limit 100


# for row in rows:
#     symbol = row['symbol']
#     symbols.append(symbol)
#     stock_dict[symbol] = row['id']


# for symbol in symbols:
#     barsets = api.get_bars(symbol, TimeFrame.Day, "2021-01-01", adjustment='raw').df
#     df = barsets
#     df['symbol'] = symbol
#     #df['stock_id'] = cursor.execute("""SELECT id FROM stock WHERE symbol = ?;""", [symbol]) ##experimental <- SHIT DOESNT FUCKING WORK
#     df.to_sql('stock_prices2', con=engine, if_exists='append')
#     print(f'processing {symbol}')
    
   
# connection.commit()


#This works, but slowly:


# import sqlite3, config
# import alpaca_trade_api as tradeapi
# from alpaca_trade_api import REST, TimeFrame
# import pandas as pd
# from sqlalchemy import create_engine

# api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)
# engine = create_engine('sqlite:///C:/Users/Bruker/Desktop/app/app.db', echo=False)

# connection = sqlite3.connect(config.DB_FILE)
# connection.row_factory = sqlite3.Row

# cursor = connection.cursor()

# cursor.execute("""
# SELECT id, symbol, name FROM stock
# """)

# rows = cursor.fetchall()


# for row in rows:
#     symbol = row['symbol']
#     barsets = api.get_bars(symbol, TimeFrame.Day, "2021-01-01", adjustment='raw').df
#     df = barsets
#     df['symbol'] = symbol
#     df['stock_id'] = row['id']
#     df.to_sql('stock_price', con=engine, if_exists='append')
#     print(f'processing {symbol}')
    
   
# connection.commit()