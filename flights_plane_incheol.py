import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#주제 자유:
# merge 사용해서 flights와 planes 병합한 데이터로
# 각 데이터 변수 최소 하나씩 선택 후 분석할 것
# 날짜&시간 전처리 코드 들어갈것
# 문자열 전처리 코드 들어갈것
# 시각화 종류 3개
# tailnum으로 merge

#fligts는 비행편   planes 비행기 정보
#flights에서 year는 비행시간
#planes에서 year는 비행기 제조년월
from nycflights13 import flights, planes
flights['datetime'] = pd.to_datetime(flights[['year','month','day','hour','minute']])
df = pd.merge(flights,planes, on ='tailnum', how='inner')
df['air_time_hour'] = df['air_time']/60
len(df['carrier'].unique())
df['distance'].min()
df.info()
df.head(3)
df['origin'].unique()
len(df['dest'].unique())

df_mu_ty = pd.DataFrame(df.groupby(['type','manufacturer'])['tailnum']
                           .count().reset_index().sort_values(by=['type', 'manufacturer', 'tailnum'], ascending=[True, True, False]))
a = df_mu_ty = pd.DataFrame(df.groupby(['carrier'])['distance'].mean())
b = df_mu_ty = pd.DataFrame(df.groupby(['manufacturer'])['air_time_hour'].sum())
c = df_mu_ty = pd.DataFrame(df.groupby(['type'])['air_time'].sum())




len(set(df['model']))  #총 127개
len(set(df['type']))  #총 127개
df_distance = pd.DataFrame(df.groupby(['manufacturer'])['distance']
                           .mean(numeric_only=True).sort_values(ascending=False)).reset_index()
print(df_distance)
df_distance_short = df_distance[df_distance['distance'] < 1000]
df_distance_mid = df_distance[(df_distance['distance'] >= 1000) & (df_distance['distance'] < 1500)]
df_distance_long = df_distance[df_distance['distance'] >= 1500]

x_s = df_distance_short['manufacturer']
y_s = df_distance_short['distance']
x_m = df_distance_mid['manufacturer']
y_m = df_distance_mid['distance']
x_l = df_distance_long['manufacturer']
y_l = df_distance_long['distance']

plt.figure(figsize=(15,6))

plt.subplot(131)
plt.plot(x_s, y_s, 'ro')
plt.xlabel('manufacturer')
plt.ylabel('distance')
plt.title('Food & Drinks service')
plt.xticks(rotation=45, fontsize=9) 

plt.subplot(132)
plt.plot(x_m, y_m, 'bo')
plt.xlabel('manufacturer')
plt.ylabel('distance')
plt.title('Drinks service')
plt.xticks(rotation=45, fontsize=9) 

plt.subplot(133)
plt.plot(x_l, y_l, 'yo')
plt.xlabel('manufacturer')
plt.ylabel('distance')
plt.title('Nothing')
plt.xticks(rotation=45, fontsize=9) 
plt.tight_layout()  # 자동으로 간격 조정
plt.show()

#####t시간별로 거리 분리

df['air_time']
df_air_time = pd.DataFrame(df.groupby(['manufacturer'])['air_time']
                           .mean(numeric_only=True)
                           .sort_values(ascending=False)).reset_index()

df_air_time_short = df_air_time[df_air_time['air_time'] < 120]
df_air_time_mid = df_air_time[(df_air_time['air_time'] >= 120) & (df_air_time['air_time'] < 240)]
df_air_time_long = df_air_time[df_air_time['air_time'] >= 240]

x_st = df_air_time_short['manufacturer']
y_st= df_air_time_short['air_time']
x_mt = df_air_time_mid['manufacturer']
y_mt = df_air_time_mid['air_time']
x_lt = df_air_time_long['manufacturer']
y_lt = df_air_time_long['air_time']

plt.figure(figsize=(15,6))

plt.subplot(131)
plt.plot(x_st, y_st, 'ro')
plt.xlabel('manufacturer')
plt.ylabel('air_time')
plt.title('Food & Drinks service')
plt.xticks(rotation=45, fontsize=9) 

plt.subplot(132)
plt.plot(x_mt, y_mt, 'bo')
plt.xlabel('manufacturer')
plt.ylabel('air_time')
plt.title('Drinks service')
plt.xticks(rotation=45, fontsize=5) 

plt.subplot(133)
plt.plot(x_lt, y_lt, 'yo')
plt.xlabel('manufacturer')
plt.ylabel('air_time')
plt.title('Nothing')
plt.xticks(rotation=45, fontsize=9) 
plt.tight_layout()  # 자동으로 간격 조정
plt.show()


#####
df.columns
df['engine'].unique()
df.plot(kind="scatter", 
        x='distance', 
        y='air_time', 
        alpha=0.6, 
        color="blue", edgecolors='black', figsize=(6,5))
