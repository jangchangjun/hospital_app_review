from datetime import datetime

from google_play_scraper import Sort, reviews
import pandas as pd

# 크롤링 대상 앱 정보
reviews_list = []
result, continuation_token = reviews(
    'com.ksncho.hospitalinfo',
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



# JSON 파일로 저장
json_file_path = 'reviews2.json'
review_df.to_json(json_file_path, orient='records', force_ascii=False, indent=4)

year = 2024
review_list_2020 = []

while year >= 2020:
    result, continuation_token = reviews(
        'com.ksncho.hospitalinfo',
        lang='ko',  # default: 'en'
        country='kr',  # default: 'us'
        sort=Sort.NEWEST,  # default: Sort.MOST_RELEVANT
        count=50000,  # default: 100
        filter_score_with=None
    )

    token = continuation_token
    year = result[-1]['at'].year

    for review in result:
        if review['at'].year >= 2020:
            temp_list_2020 = [review['score'],review['content'],review['at'].strftime('%Y-%m-%d')]
            review_list_2020.append(temp_list_2020)

review_df_2020 = pd.DataFrame(review_list_2020, columns=['score', 'content', 'date'])
print(len(review_df_2020))

json_file_path = 'reviews2_2020.json'
review_df_2020.to_json(json_file_path, orient='records', force_ascii=False, indent=4)