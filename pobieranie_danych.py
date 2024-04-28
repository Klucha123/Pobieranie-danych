import requests
import pandas as pd
import io
from datetime import datetime, date, timedelta
import json

today = date.today()
earlier = today - timedelta(days=30)

x = requests.get('https://www.pse.pl/getcsv/-/export/csv/PL_BPKD/data_od/'+str(earlier).replace("-", "")+'/data_do/'+str(today).replace("-", ""))
df = pd.read_csv(io.StringIO(x.text), sep=";")
df['Data'] = pd.to_datetime(df['Data'])
df['Data'] = df['Data'].dt.date
#open('plik.csv', 'wb').write(x.content)

y = requests.get('https://api.jao.eu/OWSMP/getauctions?corridor=PL-UA&fromdate='+str(earlier)+'&todate='+str(today)+'&horizon=Daily', headers={'AUTH_API_KEY':'b4772548-312c-48b0-ba35-84e81ce7c0bf'})
#open('plik1.csv', 'wb').write(y.content)
json_data = json.loads(y.content)
df1 = pd.DataFrame(json_data[0]['results'])
df1['date'] = datetime.strptime(json_data[0]['marketPeriodStart'][:10], '%Y-%m-%d').date()

for i in range(1,len(json_data)):
    dfy = pd.DataFrame(json_data[i]['results'])
    dfy['date'] = datetime.strptime(json_data[i]['marketPeriodStart'][:10], '%Y-%m-%d').date()
    df1 = pd.concat([df1,dfy], ignore_index=True)
# prawdopodobnie brakuje 1h ze wzgledu na zmiane czasu
df1['productHour'] = df1['productHour'].str[6:8]
df1['productHour'] = df1['productHour'].str.lstrip('0')
df1 = df1.rename(columns={'productHour': "Godzina", "date": "Data"})
df1['Godzina'] = df1['Godzina'].astype(int)
tabela = pd.merge(df, df1, on=['Data','Godzina'], how='inner')


