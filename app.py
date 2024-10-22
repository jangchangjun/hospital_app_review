from google_play_scraper import Sort, reviews_all

# 크롤링 대상 앱 정보
app_name = "com.bbros.sayup"
app_operation = reviews_all(
    app_name,
    sleep_milliseconds=0, # defaults to 20
    country="kr", # defaults to 'us'
    lang = 'ko',
    count = 500,
    sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT,

)

reviews_list = []

# 리뷰 데이터 수집
for review in app_operation:
    review_dict = {
        # 'review_id': review['review_id'],
        'review': review['content'],
        'score': review['score'],
        'thumbs_up_count': review['thumbsUpCount']
    }
    reviews_list.append(review_dict)

reviews_list.sort(key=lambda x: x['thumbs_up_count'], reverse=True)


# pandas DataFrame으로 변환
import pandas as pd
reviews_df = pd.DataFrame(reviews_list)



# JSON 파일로 저장
json_file_path = 'reviews.json'
reviews_df.to_json(json_file_path, orient='records', force_ascii=False, indent=4)


