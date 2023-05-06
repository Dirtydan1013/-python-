import requests
import pymysql

# 資料庫連線設定
conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='root',
    password='701nccumath',
    db='Fiance',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 爬取台積電(股票代號 2330)的股價資訊
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRlIjoiMjAyMy0wNS0wNiAxNjowODo1MiIsInVzZXJfaWQiOiJEaXJ0eSBkYW4iLCJpcCI6IjE0MC4xMTkuMTIxLjYifQ.E9L41Jfro4aHPswc6jZuxd5clWkvBKriDwDsj65LPbA'
url = 'https://api.finmindtrade.com/api/v4/data'
params = {
    "dataset": "TaiwanStockPrice",
    "data_id": "2330",
    "start_date": "2022-01-01",
    "end_date": "2022-05-03",
    "token": api_key
}
res = requests.get(url, params=params)

# 將資料寫入 MySQL 資料庫
for row in res.json()['data']:
    date = row['date']
    stock_id = row['stock_id']
    Trading_Volume=row['Trading_Volume']
    Trading_money=row['Trading_money']
    open = row['open']
    max =row['max']
    min = row['min']
    close = row['close']
    spread=row['spread']
    Trading_turnover=row['Trading_turnover']
    sql = f"INSERT INTO finmind (date, stock_id, Trading_Volume,Trading_money,open,max,min,close,spread,Trading_turnover) VALUES ('{date}', '{stock_id}', '{Trading_Volume}','{Trading_money}','{open}','{max}','{min}','{close}','{spread}','{Trading_turnover}')"
    cursor.execute(sql)
conn.commit()

# 關閉資料庫連線
cursor.close()
conn.close()
