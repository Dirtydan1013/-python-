import pandas as pd
import json
import requests
    
def Get_month_StockPrice(Symbol, Date ):
    date = Date
    date_time_obj = pd.to_datetime(date)
    int_date = int(date_time_obj.strftime("%Y%m%d"))
    
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={int_date}&stockNo={Symbol}&response=json&_=1691032430215'

    data = requests.get(url).text
    print(data)
    json_data = json.loads(data)

    Stock_data = json_data['data']
    

    StockPrice = pd.DataFrame(Stock_data, columns = ['Date','Volume','Volume_Cash','Open','High','Low','Close','Change','Order'])

    StockPrice['Date'] = StockPrice['Date'].str.replace('/','').astype(int) + 19110000
    StockPrice['Date'] = pd.to_datetime(StockPrice['Date'].astype(str))
    StockPrice['Volume'] = StockPrice['Volume'].str.replace(',','').astype(float)/1000
    StockPrice['Volume_Cash'] = StockPrice['Volume_Cash'].str.replace(',','').astype(float)
    StockPrice['Order'] = StockPrice['Order'].str.replace(',','').astype(float)

    StockPrice['Open'] = StockPrice['Open'].str.replace(',','').astype(float)
    StockPrice['High'] = StockPrice['High'].str.replace(',','').astype(float)
    StockPrice['Low'] = StockPrice['Low'].str.replace(',','').astype(float)
    StockPrice['Close'] = StockPrice['Close'].str.replace(',','').astype(float)

    StockPrice = StockPrice[['Date','Open','High','Low','Close','Volume']]
    return StockPrice

#return 需要的日期(往前推的)(有bug 紀地回次數)
def count_days(lastmonth_stockprice,StockPrice,date,counts,month):
    a = pd.to_datetime(date).month
    if a == month :
    # if 結束日期找得到，用索引往回推需要的收盤價
        if not StockPrice['Date'][StockPrice['Date'] == date].empty :
            datee = StockPrice['Date'][StockPrice['Date'] == date]
            index_num = datee.index.tolist()[0]
            index_num -= counts
            if index_num >= 0 :
                Date = StockPrice['Date'].loc[index_num]
                return Date
            #如果屬到的是上個月分，就去上個月份的資料下來數
            else :
                max_index = lastmonth_stockprice.index.max()
                index_num = max_index + index_num
                Date = lastmonth_stockprice['Date'].loc[index_num]
                return Date
            
        #日期找不到就一直往前推直到找到為止
        else:
            prevdate = pd.to_datetime(date) - pd.Timedelta(days=1)
            prevdate = prevdate.strftime("%Y-%m-%d")
            return count_days(lastmonth_stockprice,StockPrice,prevdate,counts,month)
    #如果不等於，去上個月的找
    else : 
        if not lastmonth_stockprice['Date'][lastmonth_stockprice['Date'] == date].empty :
                datee = lastmonth_stockprice['Date'][lastmonth_stockprice['Date'] == date]
                index_num = datee.index.tolist()[0]
                index_num -= counts
                print(index_num)
                Date = lastmonth_stockprice['Date'].loc[index_num]
                return Date
        #日期找不到就一直往前推直到找到為止
        else:
            prevdate = pd.to_datetime(date) - pd.Timedelta(days=1)
            prevdate = prevdate.strftime("%Y-%m-%d")
            return count_days(lastmonth_stockprice,StockPrice,prevdate,counts,month)
    

def find_price(date,StockPrice,lastmonth_stockprice,month):
    a = pd.to_datetime(date).month
    if  a == month :
        close_price_list = StockPrice['Close'][StockPrice['Date'] == date]
        num = close_price_list.index.tolist()[0]
        close_price = close_price_list[num]
        return close_price 
    else : 
        close_price_list =lastmonth_stockprice['Close'][lastmonth_stockprice['Date'] == date]
        num = close_price_list.index.tolist()[0]
        close_price = close_price_list[num]
        return close_price 
    
def find_close_price(Symbol, Date,count):
    #讓date的月份減少一個月，並給定本月的月份
    date1 = pd.to_datetime(Date)
    month = date1.month
    next = date1- pd.DateOffset(months=1)
    date2 = next.strftime("%Y-%m-%d")
    try:
        Stockprice = Get_month_StockPrice(Symbol,Date)
        lastmonth_stockprice = Get_month_StockPrice(Symbol, date2)
        date = count_days(lastmonth_stockprice,Stockprice,Date, count,month)
        close_price = find_price(date,Stockprice,lastmonth_stockprice,month)
        print(close_price)
        return close_price
    except :
        return 0
