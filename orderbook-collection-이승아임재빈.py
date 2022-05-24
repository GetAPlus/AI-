
import time
import datetime
import requests
import pandas as pd

book={}
Fdf=pd.DataFrame(index=range(0), columns=['price','quantity','type','timestamp'])

i=1

while(i<=43200):
        
        response=requests.get ('https://api.bithumb.com/public/orderbook/XRP_KRW/?count=5')
        book=response.json()

        data=book['data']
	
        bids=(pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
        bids.sort_values('price', ascending=False, inplace=True)
        bids=bids.reset_index(); del bids['index']
        bids['type'] =0
	
        asks=(pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
        asks.sort_values('price', ascending=True, inplace=True)
        asks=asks.reset_index(); del asks['index']
        asks['type']=1

        df=pd.concat([bids,asks])
        
        df['quantity']=df['quantity'].round(decimals=4)

        timestamp=datetime.datetime.now()
        
        req_timestamp=timestamp.strftime('%Y-%m-%d %H:%M:%S')
        fn_timestamp=timestamp.strftime('%Y-%m-%d')

        df['timestamp']=req_timestamp
        	
        print(df)

        Fdf=pd.concat([Fdf,df])

        Fdf.to_csv(fn_timestamp+"-bithumb-XRP-orderbook.csv",index=False)

        time.sleep(2)

        i=i+1
        
print('24hours collecting end')

