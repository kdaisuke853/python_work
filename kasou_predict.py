import requests
from datetime import datetime
import time
import pandas as pd
import json
import requests
from datetime import datetime
from fbprophet import Prophet

while True:

	response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=60")
	response = response.json()

	data = response["result"]["60"]

	close_time = datetime.fromtimestamp(data[0]).strftime('%Y/%m/%d %H:%M')
	open_price = data[1]
	close_price = data[4]

	print( "時間： " + close_time
		+ " 始値： " + str(open_price)
		+ " 終値： " + str(close_price) )
    
# [ CloseTime , OpenPrice , HighPrice , LowPrice , ClosePrice , Volume]
df = pd.DataFrame({'datetime': [],
                   'Openprice': [],
                   'HighPrice': [],
                   'LowPrice':[],
                   'ClosePrice':[],
                   'Volume':[],})

df_test = pd.read_csv("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=60")
df_test

response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=86400")
response = response.json()
data = response["result"]["86400"][0]

response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=86400")
response = response.json()
x = 0

	  # [ CloseTime , OpenPrice , HighPrice , LowPrice , ClosePrice , Volume]

while x < 1961:
  data = response["result"]["86400"][x]    
  close_time = datetime.fromtimestamp(data[0]).strftime('%Y/%m/%d %H:%M')
  open_price = data[1]
  high_price = data[2]
  lowPrice = data[3]
  close_price = data[4] 
  volume = data[5]
  df.loc[x] = [close_time,open_price,high_price,lowPrice,close_price,volume]
  x += 1
  
  df.to_csv('kasou.csv')
  
response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=86400")
response = response.json()
data_all = response["result"]["86400"][1961]
close_time = datetime.fromtimestamp(data_all[0]).strftime('%Y/%m/%d %H:%M')
close_time

response = requests.get("https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?periods=86400")
response = response.json()
data_all = response["result"]["86400"][-2]
close_time = datetime.fromtimestamp(data_all[0]).strftime('%Y/%m/%d %H:%M')
close_time

#高値をyに
df = df.rename(columns={'HighPrice': 'y'})
df

df = df.rename(columns={'datetime': 'ds'})

model = Prophet()

model.fit(df)

future = model.make_future_dataframe(periods=200, freq='H')

future.tail()
  
forecast = model.predict(future)
forecast


