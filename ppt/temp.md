# **탑승률과 항공편 지연 분석 보고서**

## **1. 사용 데이터**
| 데이터셋       | 설명                                       | 주요 컬럼 |
|----------------|--------------------------------------------|----------------|
| `flights.csv`  | 항공편 정보 (출발지, 도착지, 지연 시간 등) | `flight`, `carrier`, `origin`, `dest`, `dep_delay`, `arr_delay`, `distance`, `year`, `month` |
| `planes.csv`   | 항공기 정보 (제조 연도, 모델 등)           | `tailnum`, `manufacturer`, `model`, `year` |
| `airlines.csv` | 항공사 코드 및 항공사명 정보               | `carrier`, `name` |
| `T-100.csv`    | 미국 국내선 항공사의 운항 실적 (항공편 수, 좌석 수, 승객 수, 운항 거리 등) | `year`, `month`, `carrier`, `origin`, `dest`, `seats`, `passengers` |

## **2. 데이터 전처리**
1. **데이터 병합 및 컬럼 정리**
   - `flights.csv`와 `planes.csv`를 `tailnum`을 기준으로 병합
   - `airlines.csv`를 `carrier` 기준으로 병합하여 항공사명 추가
   - `datetime` 컬럼을 생성 (`year`, `month`, `day`, `hour`, `minute`를 변환)
   - 불필요한 컬럼(`speed`) 제거

2. **탑승률 계산을 위한 데이터 전처리**
   - `T-100.csv`에서 **NYC 공항(LGA, JFK, EWR)만 필터링**
   - `dest`가 기존 `flights.csv`의 목적지 목록에 있는 데이터만 남김
   - `carrier`가 기존 `flights.csv`에 존재하는 항공사만 남김
   - `year`, `month`, `carrier`, `origin`, `dest` 기준으로 `seats`, `passengers` 합산
   - `flights.csv`를 같은 기준으로 그룹화하여 `flight_count`, `avg_dep_delay`, `avg_arr_delay`, `total_distance` 계산
   - 두 데이터 병합 후 **탑승률(Load Factor) 계산:** `passengers / seats`

3. **이상치 제거**
   - 출발 지연(`avg_dep_delay`)에서 IQR을 이용한 이상치 제거
   - 도착 지연(`avg_arr_delay`)에서도 동일한 방식 적용

## **3. 분석 목적**
이 연구의 목표는 **탑승률(Load Factor)이 높은 항공편이 지연될 가능성이 더 높은지 분석**하는 것이다.  
탑승률이 높을수록 승객 탑승 절차가 길어지고, 수하물 처리 시간이 증가하며, 출발 준비 시간이 지연될 가능성이 있기 때문에 이를 검증하는 것이 주요 목적이다.

## **4. 가설**
> **"좌석 점유율(탑승률)이 높을수록 항공편 지연 시간이 증가할 것이다."**

## **5. 분석 및 시각화**
### **(1) 산점도를 통한 관계 분석**
```python
plt.figure(figsize=(10, 6))
sns.scatterplot(data=cleaned_df, x="load_factor", y="avg_dep_delay", alpha=0.5)
plt.xlabel("Load Factor")
plt.ylabel("Average Departure Delay")
plt.title("Load Factor vs Average Departure Delay (Outliers Removed)")
plt.axhline(0, color="gray", linestyle="--")
plt.show()
```
### **(2) 선형 회귀선을 포함한 시각화**
```python
plt.figure(figsize=(10, 6))
sns.scatterplot(data=cleaned_df, x="load_factor", y="avg_dep_delay", alpha=0.5, label="Data")
sns.regplot(data=cleaned_df, x="load_factor", y="avg_dep_delay", scatter=False, color="red", line_kws={"linewidth":2}, label="Trend Line")
plt.xlabel("Load Factor")
plt.ylabel("Average Departure Delay")
plt.title("Load Factor vs Average Departure Delay (With Trend Line)")
plt.axhline(0, color="gray", linestyle="--")
plt.legend()
plt.show()
```
### **(3) 탑승률 구간별 평균 지연 시간 분석**
```python
cleaned_df["load_factor_bin"] = pd.cut(cleaned_df["load_factor"], bins=[0, 0.3, 0.5, 0.7, 0.9, 1], labels=["0-30%", "30-50%", "50-70%", "70-90%", "90-100%"])
summary_stats = cleaned_df.groupby("load_factor_bin")[["avg_dep_delay", "avg_arr_delay"]].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=summary_stats, x="load_factor_bin", y="avg_dep_delay", marker="o", label="출발 지연 (분)", color="blue")
sns.lineplot(data=summary_stats, x="load_factor_bin", y="avg_arr_delay", marker="s", label="도착 지연 (분)", color="red")
plt.xlabel("Load Factor (탑승률) 범위")
plt.ylabel("평균 지연 시간 (분)")
plt.title("탑승률에 따른 평균 출발/도착 지연 시간")
plt.legend()
plt.grid(True)
plt.show()
```

## **6. 결과**
- **탑승률이 낮은 항공편(0-30%)은 출발 지연이 적고, 도착은 오히려 빨라지는 경향을 보임**
- **탑승률이 50%를 넘어서면서부터 출발 및 도착 지연 시간이 증가하는 패턴이 나타남**
- **탑승률이 높은 항공편(90-100%)은 출발 지연이 가장 크며(평균 14.2분), 도착 지연도 가장 높음(평균 7.7분)**
- **탑승률과 출발 지연의 상관관계 분석 결과, 중간 정도의 양의 상관관계를 가짐 (상관계수 0.5~0.6 수준)**

## **7. 결론**
이 연구를 통해 **탑승률이 높을수록 항공편 지연이 증가하는 경향이 확인됨**.  
특히 만석(90-100%) 항공편의 경우 출발 및 도착 지연이 평균적으로 더 높아지는 패턴을 보임.  
이는 **탑승 인원 증가로 인한 수하물 처리, 탑승 절차 지연, 게이트 대기 시간 증가 등의 복합적인 요인이 영향을 미쳤을 가능성이 높음**.  
추가적으로 **공항별 혼잡도, 시간대별 지연 패턴을 포함한 심층 분석이 필요함.**

