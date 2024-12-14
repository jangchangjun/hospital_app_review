# KOELECTRA를 활용한 병원 원격진료 앱 리뷰 감성 분석

## 1. 개요

### 1.1 문제정의

최근 여러 병원들은 전문의 부족으로 인해 소아청소년 응급실 야간 진료를 중단하거나 진료 시간을 감축하는 등의 조치를 취하고 있다. 이로 인해 한정적인 진료 시간대에 많은 사람들이 모여들게 되었고, 이는 곧 긴 대기 시간으로 이어지게 되었다. 소아과 오픈런은 물론이며 4-5시간 대기 후에 진료를 받는 일도 일상이 되었다. 이러한 상황 속 똑닥은 모바일 진료 예약 기능을 통해 순식간에 부모들의 육아 필수 앱이 되었다.[[1]](https://www.medicaltimes.com/Main/News/NewsView.html?ID=1112939)  
똑닥은 무료 진료 예약 서비스로 큰 인기를 끌었으며, 여러 병원 또한 똑닥과 제휴를 맺을 정도로 크게 성장해 나갔다.

<div> <img src = "img/ddodoc.jpg" width="400"> <img src = "img/ddodoc2.jpg" width="250", height = "400"> </div>


하지만 유료 서비스로 전환된 뒤, 앱에 대한 평가는 월 1000원으로 이 정도 서비스면 결제할 의향이 있다는 긍정적인 의견, 공립이 아닌 사기업을 통한 병원 예약은 의료 민영화로 이어질 수 있다. 또는 진료 예약에도 돈을 내야 하는 것에 불만이 있는 부정적인 의견으로 나뉘게 되었다.[[2]](https://www.ibabynews.com/news/articleView.html?idxno=112206)
이 프로젝트에서는 앱 리뷰 데이터를 통해 긍·부정을 판별하는 인공지능 모델을 만들고, 학습을 통해 판별된 데이터로 사용자의 리뷰를 분석해 이를 기반으로 서비스 개선 방안을 제시할 수 있는 프로그램을 만들고자 한다.

### 1.2 데이터 및 모델 개요

데이터는 구글 플레이 앱스토어에서 제공하는 똑닥 리뷰를 크롤링한 약 1만 2천 건의 데이터를 활용해 사전 학습 모델의 재학습을 진행하고자 한다.

| 입력 | 모델 |출력|
|----------|---|---|
| 똑닥 리뷰 문장 | KoELECTRA-Small-v3 <sup>[[3]](https://huggingface.co/monologg/koelectra-small-discriminator)</sup> |부정(0), 긍정(1)|

똑닥 리뷰 데이터셋의 수집 기간은 2015년 2월부터 2024년 11월이며, 구글 플레이 스토어에 있는 리뷰를 수집하여 만들었다. 학습을 진행할 모델은 KOELECTRA로 최고 수준의 한국어 자연어 처리 모델 중 하나이다. 이 프로젝트에서는 koelectra-small-v3 모델을 활용하였다.

## 2. 데이터

### 2.1 탐색적 데이터 분석

| |score| content |date|
|-|----------|---|--|
|0|5|굿| 2024-11-18 |
|1|1|시간 예약 안 됨...그럴꺼면 유료어플 하지마라 아니면 시간예약을 받던지 개선 필요| 2024-11-18 |
|2|5|좋음| 2024-11-15 |
|3|4|편리해요| 2024-11-14 |
|..|...|...|...| .. |
|12254|5|깔끔해서 쉽게 찾을 수 있고 카톡 페이스북계정이라 쉽게 이용할 수 있어서 좋아요~~| 2015-02-02 |
|12255|5|페북 보구 깔아봤는데 겁나 유용하네요ㅇㅇ 대학생이면 특히 추천쌔림ㅇㅇ| 2015-02-02 |
|12256|5|실질적인 혜택들이 많네요... 굿~~!| 2015-02-02 |

12257건의 데이터로 이루어져있으며 score, content, date 열로 구성되어있다. 

<div><p align='center'><img src="img/scores.png" width = "550", height = "400"></p></div>

score열은 1-5점의 평점으로 이루어져있으며, 최고점인 5점이 약 10000건 최저점인 1점이 약 1400건으로 구성되어있다.

### 2.2 데이터 전처리

제일 먼저 데이터의 결측치를 확인해본 결과, 데이터의 결측치는 없는 것으로 나타났다.

```
print('결측치 = ', data.isnull().values.sum())
data = data.dropna(how = 'any')
print('데이터 개수', len(data)
```

```
결측치 =  0
데이터 개수 12257
```

데이터 전처리를 진행하며 데이터셋이 크지 않아 결측치를 제외한 추가적인 규정사항을 두지 않았다. 데이터셋에 라벨이 존재하지 않아 score 열을 이용해 4-5는 긍정(1), 1-2는 부정(0)으로 두어 라벨링을 진행하였으며 보다 정확한 학습을 위해 3점의 score를 가진 데이터는 제외하였다.

- 최종데이터 셋.

| | score | content | date | label |
|-|----------|---|--|--|
|0|1|Galaxy 24 Ultra 와 galaxy 24 Plus 집에 세대 있는데 다 8월 이후 똑딱 QR코드 처방전 등록이 안됨. 잘 되다가 갑자기 안 되는 이유를 모르겠고 빨리 수정 바람. 삭제하고 다시 깔아도 안됨| 2024-11-24 | 0 |
|1|5|시간절약| 2024-11-23 | 1 |
|2|1|똑딱 대기번호와 실제 대기번호가 다릅니다. 병원에서는 똑딱시스템에 대해 잘 모르던데 병원과 연계가 부족한듯합니다.| 2024-11-22 | 0 |
|3|1|사용 불편| 2024-11-19 | 0 |
|..|...|...|...| .. | .. |
|12254|5|깔끔해서 쉽게 찾을 수 있고 카톡 페이스북계정이라 쉽게 이용할 수 있어서 좋아요~~| 2015-02-02 | 1 |
|12255|5|페북 보구 깔아봤는데 겁나 유용하네요ㅇㅇ 대학생이면 특히 추천쌔림ㅇㅇ| 2015-02-02 | 1 |
|12256|5|실질적인 혜택들이 많네요... 굿~~!| 2015-02-02 | 1 |

- 데이터 전처리 후 긍 부정 비율.

<div><p align='center'><img src="img/circle.png" width = "400", height = "400"></p></div>

데이터 전처리 후 긍 부정비율이다. 총 데이터셋에서 긍정이 약 86% 부정이 약 14% 인것으로 나타났다.

- 랜덤 학습데이터 추출

모델의 학습을 위해 랜덤으로 데이터를 추출해 샘플 데이터셋을 만들었다. 보다 더 유의미한 프로젝트를 위해 score 열만을 이용한 라벨링 데이터셋과 score를 기준으로 라벨링한 뒤 직접 다시 라벨링을 진행한 데이터셋을 준비하였으며 두 개의 샘플 데이터 모두 전체 데이터셋의 긍·부정 비율을 고려해 1:3 비율로 추출을 진행하였다.

- score를 이용한 학습데이터

| | score | content | date | label |
|-|----------|---|--|--|
|0|5|우리아기 병원예약 늘 똑딱으로 해서 다니고있어요. 편리합니다^^| 2021-10-12	| 1 |
|1|5|너무 편리하고 좋아요!| 2019-12-28 | 1 |
|..|...|...|...| .. | .. |
|1998|1|처음가는 병원 똑딱으로 접수해도 주민번호 다시 불러야되던데 그럼 굳이 똑딱에는 주민뒷번호 까지 왜 수집함? 니들이 뭔데? 남의정보 수집함??| 2015-02-02 | 0 |
|1999|1|쓰지마삼 약국 1도 안뜸ㅋㅋ| 2015-02-02 | 0 |

- 학습과 검증 데이터셋 분리

<div><img src="img/학습1.png"></div>

<div><img src="img/sample_1_데이터분리.png"></div>

긍정 데이터 1500개와 부정 데이터 500건을 랜덤으로 추출해 총 2000건으로 이루어져있으며,
학습 데이터 1600개와 검증 데이터 400개로 분리하였다.

- 직접 라벨링을 거친 학습데이터

직접 라벨링을 진행하며 리뷰 글자 수가 20자 이상, 평점이 4-5점 이지만 부정적인 내용이 담겨있거나 1-2점인데 긍정적인 내용이 담겨있던 열을 삭제하였고, 어플과 관련없는 리뷰, 별점과 내용이 알맞지 않는 경우에 데이터를 삭제하였다.

ex)

| | score | content | date | label |
|-|----------|---|--|--|
|0|4|병원 검색을 매번 해야해서 번거롭..즐찾하는 기능이 있는거같은데 어려워영.. 알람이 매우 자주 와서 병원 방문을 절대 까먹진 않을 듯요| 2023-11-07	| 1 |
|1|5|Good| 2016-07-16 | 1 |
|2|5|갈수록 복잡해 지는것 같아요 초기버전이 간단해서 좋았네요| 2020-03-04 | 1 |

#### 과정을 거친 학습 데이터

| | score | content | date | label |
|-|----------|---|--|--|
|0|5|병원 검색할때 찾기 쉽고 똑딱쓰는 병원은 예약하기 편하고 좋아요. 여러 병원이 이용했음 좋겠어요| 2022-11-07	| 1 |
|1|5|바라던 앱에다 이름까지 귀엽고!이 앱 만들어주셔서 감사해요♡| 2016-06-16 | 1 |
|..|...|...|...| .. | .. |
|1298|1|병원 예약을 돈내고 앱을 통해 하게 만들고 돈 없거나 앱 쓸줄 모르는 사람들은 의료혜택 차별받게 하는 양아치 앱. 사용하지 않아야 합니다. 앱 기획의도 자체가 쓰레기 같네요. 먼저 간 사람이 먼저 검진하는게 당연합니다. 앱 삭제 하세요| 2023-12-05 | 0 |
|1299|1|	처음 설치해봤는데 환자명에 다른 사람이름이 있었어요. 제 정보로 수정했는데 계속해서 그 분 정보로 바뀌더라구요. 카카오연동후에 그러는거 같은데 오류인가요? 좀 무섭네요.| 2020-02-04 | 0 |

- 학습과 검증 데이터셋 분리

<div><img src="img/학습2.png"></div>

<div><img src="img/sample_2_데이터분리.png"></div>

긍정 데이터 1000건과 부정 데이터 300건을 랜덤으로 추출해 총 1300건으로 이루어져있으며,
학습 데이터 1040개와 검증 데이터 260개로 분리하였다.

## 3. 재학습 결과
### 3.1 개발환경
<img src="https://img.shields.io/badge/pycharm-000000?style=flat-square&logo=pycharm&logoColor=white"/> <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/torch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/> <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white"/> <img src="https://img.shields.io/badge/numpy-013243?style=flat-square&logo=numpy&logoColor=white"/> <img src="https://img.shields.io/badge/transformers-81c147?style=flat-square&logo=transformers&logoColor=white"/> <img src="https://img.shields.io/badge/scikit-learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white"/>

## 3.2 KOELECTRA fine-tuning

KOELECTRA 모델을 fine-tunning하며 각각 2000건, 1300건의 데이터를 학습 데이터를 사용했으며, 데이터를 학습시킨 뒤 총 12257건의 데이터에 적용시켜 모델을 테스트했다.

## 3.3 학습 결과 그래프

<div><p align='center'><img src="img/검증정확도_1.png"></p></div>

<div><p align='center'><img src="img/학습오차.png"></p></div>

<table>
  <tr align="center"><th></th><th></th><th>Epoch 1</th><th>Epoch 2</th><th>Epoch 3</th><th>Epoch 4</th></tr>
  <tr align="center"><th rowspan="2">학습데이터 1</th><td>평균 학습 오차</td><td>0.40</td><td>0.25</td><td>0.20</td><td>0.15</td></tr>
  <tr align="center"><td>검증 정확도</td><td>0.86</td><td>0.91</td><td>0.90</td><td>0.90</td></tr>
</table>

학습 데이터의 평균 오차가 학습이 진행됨에 따라 0.40에서 0.15로 감소하였였고 이와 반대로 검증 정확도는 학습이 진행됨에 따라 0.86에서 0.90까지 상승하였다.

<div><p align='center'><img src="img/검증정확도_2.png"></p></div>

<div><p align='center'><img src="img/학습오차_2.png"></p></div>

<table>
  <tr align="center"><th></th><th></th><th>Epoch 1</th><th>Epoch 2</th><th>Epoch 3</th><th>Epoch 4</th></tr>
  <tr align="center"><th rowspan="2">학습데이터 2</th><td>평균 학습 오차</td><td>0.30</td><td>0.20</td><td>0.10</td><td>0.03</td></tr>
  <tr align="center"><td>검증 정확도</td><td>0.92</td><td>0.98</td><td>0.99</td><td>0.99</td></tr>
</table>

학습 데이터의 평균 오차가 학습이 진행됨에 따라 0.30에서 0.03로 감소하였였고 이와 반대로 검증 정확도는 학습이 진행됨에 따라 0.92에서 0.99까지 상승하였다.

두 개의 학습데이터 모두 높은 정확도와 낮은 오차율을 보였지만, score열만을 활용한 학습 데이터보다 직접 라벨링을 진행한 두 번째 학습 데이터의 정확도가 더 높게 나타났다.

## 3.4 모델 적용

각각의 학습 모델을 전체 데이터(12,257건)에 적용한 결과

학습 데이터1

```
Test step : 1/371, Temp Accuracy : 0.78125
Test step : 2/371, Temp Accuracy : 0.90625
Test step : 3/371, Temp Accuracy : 0.84375
...
Test step : 369/371, Temp Accuracy : 0.9375
Test step : 370/371, Temp Accuracy : 1.0
Test step : 371/371, Temp Accuracy : 1.0
Total Accuracy : 0.9182951482479784
```

학습 데이터2

```
Test step : 1/371, Temp Accuracy : 0.78125
Test step : 2/371, Temp Accuracy : 0.875
Test step : 3/371, Temp Accuracy : 0.875
...
Test step : 369/371, Temp Accuracy : 0.9375
Test step : 370/371, Temp Accuracy : 1.0
Test step : 371/371, Temp Accuracy : 1.0
Total Accuracy : 0.926128706199461
```

## 4. 모델 적용 데이터 활용.

위 단계에선 앞서 학습한 데이터를 토대로 사용자 경험을 기반으로한 서비스 개선 방안을 제안하는 과정을 보여주고자 한다.
이 단계에선 두 개의 모델중 정확도가 더 높았던 2번째 모델이 예측한 데이터셋을 활용할 것이다.

### 4.1 데이터 분석

데이터를 연,월별로 분석한 뒤 확실한 결과를 얻기 위해 큰 변화폭을 가진 데이터에 집중해 분석을 진행할 것이다.

#### 연별 리뷰

<div><p align='center'><img src="img/년별리뷰슈.png" width = "500", height = "400"></p></div>

데이터를 수집한 2015년 부터 2024년까지의 리뷰수 분포 그래프이다.

그래프에 보이다시피 코로나가 발발한 2019년도의 리뷰수가 압도적으로 많고, 그 뒤로 2020, 2022, 2023년이 뒤따라 오는것을 알 수 있다.

<div><p align='center'><img src="img/년별긍부정.png" width = "500", height = "400"></p></div>

연별 리뷰의 긍부정 분포 그래프이다.

2015, 2019, 2020년의 리뷰는 긍정이 많은 반면 2017,2023, 2024년의 리뷰는 부정 비율이 많은 것을 알 수 있다.

#### 월별 리뷰

앞서 말했듯, 큰 변화폭을 가진 2017, 2019, 2024년도의 데이터에 대해 집중적으로 분석할 것이다.

- 2017
  
<div><p align='center'><img src="img/2017리뷰수.png" width = "500", height = "400"></p></div>
<div><p align='center'><img src="img/2017긍부정.png" width = "500", height = "400"></p></div>

2017년의 리뷰 수는 1월에 집중되어있으며, 긍부정 비율은 2, 3월과 7월 이후에 긍정과 부정의 비율이 비슷하거나 부정의 비율이 더 많아진 것을 알 수 있다.

- 2019

<div><p align='center'><img src="img/2019리뷰수.png" width = "500", height = "400"></p></div>
<div><p align='center'><img src="img/2019긍부정.png" width = "500", height = "400"></p></div>

2019년 그래프의 리뷰수는 12월달에 집중되어있으며, 모든 월이 긍정의 비율이 압도적으로 많았다.
이는 코로나 펜데믹 시절 똑닥의 서비스에 사용자 대부분의 만족도가 높았음을 시사한다.

- 2024

<div><p align='center'><img src="img/2024리뷰수.png" width = "500", height = "400"></p></div>
<div><p align='center'><img src="img/2024긍부정.png" width = "500", height = "400"></p></div>

2024년의 리뷰 수 또한 1월에 집중되어있으며 2, 3, 5, 6, 9월달을 제외하면 부정의 비율이 긍정과 비슷하거나 더 많은 것을 알 수 있다.

### 4.3 사용자 유입/이탈 분석

위 그래프의 긍정 및 부정 결과를 바탕으로, 사용자들이 앱의 어떤 점을 긍정적으로 평가하거나 부정적으로 인식했는지를 토픽 모델링을 통해 분석해보고자 한다.

긍·부정 리뷰를 각 년도별로 5등분하여 토픽 모델링을 진행하였으며, 특정 단어가 많이 나올수록 글자의 크기를 늘려 워드 클라우드 형태의 그래프로 표현하였다.

- 2017
  
<div> <img src = "img/2017_부정1.png" width="330", height = "200"> <img src = "img/2017_부정2.png" width="330", height = "200"> <img src = "img/2017_부정3.png" width="330", height = "200"> </div>

2017년의 부정 토픽에서는 "불편", "검색", "최악", "인증" 등의 단어가 두드러지게 나타났다. 이 결과를 통해 2017년 사용자들은 똑닥앱의 인증 절차와 근처 병원 및 약국 검색에서 큰 불편함을 느꼈음을 알 수 있다.

- 2019
  
<div> <img src = "img/2019_긍정1.png" width="330", height = "200"> <img src = "img/2019_긍정2.png" width="330", height = "200"> <img src = "img/2019_긍정3.png" width="330", height = "200"> </div>

2019년의 긍정 토픽에서는 "편리", "대기", "소아과", "방문", "유용" 등의 단어가 두드러지게 나타났다. 이 결과를 통해 2019년 사용자들은 코로나 팬데믹으로 인해 병원을 찾는 사람들이 많아지면서 대기 시간이 기하급수적으로 늘어나는 상황에서, 원격 진료 접수가 가능한 똑닥앱을 활용해 편리함을 느꼈음을 알 수 있다. 특히, 소아과에 직접 방문하지 않고 원격으로 접수할 수 있는 점과 대기 시간을 알려주는 기능 덕분에 집에서 편안하게 기다릴 수 있다는 긍정적인 의견이 많았다.

- 2024
  
<div> <img src = "img/2024_부정1.png" width="330", height = "200"> <img src = "img/2024_부정2.png" width="330", height = "200"> <img src = "img/2024_부정3.png" width="330", height = "200"> </div>

2024년의 부정 토픽에서는 "유료", "이용", "시간", "인증" 등의 단어가 두드러지게 나타났다. 2023년 9월부터 똑닥이 유료 멤버십을 시작하면서, 많은 리뷰에서 사기업이 병원 접수 체제를 점령하는 의료 민영화에 대한 부정적인 시각이 드러났다. 또한 앱을 이용하는 사람이 많아짐에 따라 원격 접수 시 소요되는 시간이 길어지는 점과 2017년과 마찬가지로 인증 과정의 번거로움에 대한 부정적인 의견이 많았다.

### 4.4 기대 효과

위와 같은 사용자 리뷰 기반의 감성 분석 프로젝트를 통해 기업은 사용자의 피드백을 통해 서비스의 장점과 단점을 명확히 파악할 수 있으며, 어떤 점을 강조해야 하고 어떤 점을 개선해야 할지를 분명히 알 수 있다. 또한, 추가적인 리뷰를 계속 분석함으로써 지속적인 개선이 가능해지며, 이러한 과정은 장기 사용자 확보, 새로운 사용자 유입, 그리고 사용자의 이탈률을 줄이는 데 기여하여 안정적인 수익 모델로써의 긍정적인 역할을 할 수 있다.


## 5. 결론 및 느낀점

이번 감성 분석 프로젝트를 통해 직접 리뷰 데이터를 수집하고 가공하여 데이터셋을 만드는 경험을 하게 되었고, 보다 의미 있는 학습을 위한 샘플 데이터를 직접 추출하는 과정을 통해 프로젝트가 더욱 심도 있게 진행된 것 같아 매우 좋았다. 단순한 데이터 분석에 그치지 않고, 모델이 예측한 데이터를 바탕으로 앱의 개선 방안을 제시할 수 있는 기회를 얻은 점이 특히 인상 깊었다.
이러한 경험을 통해 데이터 분석이 그저 "분석"의 단계에서 그치지 않고 실제 사용자의 경험을 통해 어플의 단점을 개선하고 장점을 살려줄 수 있는 중요한 장치임을 깨닫게 되었다.

































































