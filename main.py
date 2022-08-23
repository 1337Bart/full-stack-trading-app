import sqlite3, config
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI() #instance of fastApi app
templates = Jinja2Templates(directory="templates") #configuring a template directory

#uvicorn main:app --reload to start the app and update the changes, also to get the port

@app.get("/") #all get requests to this route will get routed to this function. Whatever response the function returns, will be returned to the app
def index(request: Request):
    
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row #this makes SQLite return sqlite Row objects
    cursor = connection.cursor()

    cursor.execute("""SELECT id, symbol, name FROM stock ORDER BY symbol""") 

    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


#dynamic routing to symbols
@app.get("/stock/{symbol}") 
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row #this makes SQLite return sqlite Row objects
    cursor = connection.cursor()

    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""", (symbol,))

    row = cursor.fetchone()

    cursor.execute("""SELECT * FROM stock_price WHERE stock_id = ? ORDER BY timestamp DESC""", (row['id'],))
    
    prices = cursor.fetchall()
    

    #Prawdopodobnie nie moze dostac ROW i PRICES z jakiegos powodu???

    
    
    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})   