from app_store_scraper import AppStore
import pandas as pd
from pprint import pprint

tistory = AppStore(country="kr", app_name="똑닥-병원-예약-접수-필수-앱-약국찾기")
tistory.review(how_many=3)
pprint(tistory.reviews)
pprint(tistory.reviews_count)

pd.DataFrame(tistory.reviews)