import pandas as pd 
from fcdb2 import find_close_price
import time

df = pd.read_excel('op6.xlsx')

list1 = df['代碼'].tolist() 
list2 = df['開始日期'].tolist() 
list3 = df['結束日期'].tolist()

for i in range(len(list2)):
    date_time_obj1 = pd.to_datetime(list2[i])
    date_time_obj2 = pd.to_datetime(list2[i])
    list2[i] = date_time_obj1.strftime('%Y-%m-%d')
    list3[i] = date_time_obj2.strftime('%Y-%m-%d')
    
df['開始日期'] = list2
df['結束日期'] = list3

column_names = ['前一天收盤價', '前三天收盤價', '前五天收盤價' ,'前七天收盤價']
df1 = pd.DataFrame(columns=column_names)

for i in range(len(list2)):
    close_price = find_close_price(str(list1[i]),str(list2[i]),1)
    df1.loc[i] =  close_price
    print(close_price)
    time.sleep(5)
    
print(df1)
df1.to_excel('price.xlsx', index=False)

