import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_excel('data.xlsx')

df['年份'] = df['年份'].astype(int)

model = ARIMA(df['人口数'], order=(1, 1, 0))
results = model.fit()

forecast = results.get_forecast(steps=5)
predictions1 = forecast.predicted_mean

print(predictions1)


df['年份'] = df['年份'].astype(int)

model = ARIMA(df['比重'], order=(1, 1, 0))
results = model.fit()

forecast = results.get_forecast(steps=5)
predictions2 = forecast.predicted_mean

print(predictions2)

df['年份'] = df['年份'].astype(int)

model = ARIMA(df['老年抚养比'], order=(1, 1, 0))
results = model.fit()

forecast = results.get_forecast(steps=5)
predictions3 = forecast.predicted_mean

print(predictions3)

df['年份'] = df['年份'].astype(int)

model = ARIMA(df['享受老年人补贴（人）'], order=(1, 1, 0))
results = model.fit()

forecast = results.get_forecast(steps=5)
predictions4 = forecast.predicted_mean

print(predictions4)
