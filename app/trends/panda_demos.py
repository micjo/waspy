import pandas as pd

index = pd.DatetimeIndex(['00:00:0', '00:00:1', '00:00:2', '00:00:3'])

data = pd.read_csv('data.csv', infer_datetime_format=True)

idx = pd.date_range('2021-01-14 00:00:00', '2021-01-14 00:00:10', freq='2S')


data['timestamp'] = pd.to_datetime(data['timestamp'])
data['timestamp'] = data['timestamp'].dt.floor('s')
# data = data.set_index(['timestamp'])
# print(data.index.name)
print(data.loc[data['timestamp'].isin(idx)].to_json(orient="records"))

