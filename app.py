from google_play_scraper import Sort, reviews
import pandas as pd
import json

# 크롤링 대상 앱 정보
reviews_list = []
result, continuation_token = reviews(
    'com.bbros.sayup',
    lang='ko',  # default: 'en'
    country='kr',  # default: 'us'
    sort=Sort.NEWEST,  # default: Sort.MOST_RELEVANT
    count=50000,  # default: 100
    filter_score_with=None  # default: None (모든 평점을 다 가져옴)
)
for review in result:
    temp_list = [review['score'],review['content'],review['at'].strftime('%Y-%m-%d')]
    reviews_list.append(temp_list)

review_df = pd.DataFrame(reviews_list, columns=['score', 'content', 'date'])
review_df.dropna()
print(review_df)


# JSON 파일로 저장
json_file_path = 'reviews.json'
review_df.to_json(json_file_path, orient='records', force_ascii=False, indent=4)

# year = 2024
# review_list_2020 = []
#
# while year >= 2020:
#     result, continuation_token = reviews(
#         'com.bbros.sayup',
#         lang='ko',  # default: 'en'
#         country='kr',  # default: 'us'
#         sort=Sort.NEWEST,  # default: Sort.MOST_RELEVANT
#         count=50000,  # default: 100
#         filter_score_with=None
#     )
#
#     token = continuation_token
#     year = result[-1]['at'].year
#
#     for review in result:
#         if review['at'].year >= 2020:
#             temp_list_2020 = [review['score'],review['content'],review['at'].strftime('%Y-%m-%d')]
#             review_list_2020.append(temp_list_2020)
#
# review_df_2020 = pd.DataFrame(review_list_2020, columns=['score', 'content', 'date'])
# print(len(review_df_2020))

# excel_file = 'labeld.xlsx'
# df = pd.read_excel(excel_file)
#
# # 텍스트 파일로 저장 (출력 파일명을 설정하세요)
# labeled_json = 'labeled.json'
# df.to_json(labeled_json, orient='records', force_ascii=False, indent=4)
#
input_file = "reviews.txt"
output_file = "labeled_reviews.txt"

# 데이터 불러오기
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# DataFrame 변환
df = pd.DataFrame(data)

# 라벨링: score가 4, 5면 긍정(1), 1, 2면 부정(0), 나머지 제외
df = df[df['score'].isin([1, 2, 4, 5])]  # 중립인 3점 데이터 제외
df['label'] = df['score'].apply(lambda x: 1 if x >= 4 else 0)

# 결과 저장
df.to_csv(output_file, sep='\t', index=False, encoding='utf-8')
print(f"라벨링된 데이터가 {output_file}에 저장되었습니다.")






