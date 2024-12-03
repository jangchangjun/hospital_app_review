import pandas as pd
import matplotlib.pyplot as plt
import platform

df = pd.read_json('./reviews.json')
df2 = pd.read_json('./reviews2.json')
df_2020 = pd.read_json('./reviews_2020.json')
df_2_2020 = pd.read_json('./reviews2_2020.json')
labeled = pd.read_json('./labeled.json')
df_2017 = pd.read_json('./reviews_2017.json')


df['label'] = df['score'].apply(lambda x: 'positive'
                                        if x >= 4 else('negative' if x <3 else "neutral"))

df2['label'] = df['score'].apply(lambda x: 'positive'
                                        if x == 5 else('negative' if x <3 else "neutral"))


df_2020['label'] = df_2020['score'].apply(lambda x: 'positive'
                                        if x == 5 else('negative' if x <3 else "neutral"))

df_2_2020['label'] = df_2_2020['score'].apply(lambda x: 'positive'
                                        if x == 5 else('negative' if x <3 else "neutral"))

df_2017['label'] = df_2017['score'].apply(lambda x: 'positive'
                                        if x == 5 else('negative' if x <3 else "neutral"))

labeled['label'] = labeled['label'].apply(lambda x: 1
                                        if x == "긍" else 0  )

df['label'] = df['label'].apply(lambda x: 1 if x == "positive" else 0)

df2['label'] = df2['label'].apply(lambda x: 1 if x == "positive" else 0)

df_2020['label'] = df_2020['label'].apply(lambda x: 1 if x == "positive" else 1)

df_2_2020['label'] = df_2_2020['label'].apply(lambda x: 1 if x == "positive" else 1)

df_2017['label'] = df_2017['label'].apply(lambda x: 1 if x == "positive" else 1)

positive_sample_2 = labeled[labeled['label']==1].sample(n = 1000, random_state=42)
negative_sample_2 = labeled[labeled['label']==0].sample(n = 300, random_state=42)

sample_2 = pd.concat([positive_sample_2, negative_sample_2])
sample_2.to_csv('sample_2.csv', index=False)

positive_sample_1 = df[df['label']==1].sample(n = 1500, random_state=42)
negative_sample_1 = df[df['label']==0].sample(n = 500, random_state=42)

sample_1 = pd.concat([positive_sample_1, negative_sample_1])
sample_1.to_csv('sample_1.csv', index=False)


import pandas as pd


# CSV 파일을 텍스트 파일로 저장하는 함수
def save_csv_as_txt(csv_file_path, txt_file_path):
    # CSV 파일을 DataFrame으로 불러오기
    df = pd.read_csv(csv_file_path)

    # TXT 파일로 변환하여 저장
    df.to_csv(txt_file_path, index=False, sep='\t')


# 사용 예시
csv_file_path = 'sample_2.csv'  # 읽어올 CSV 파일 경로
txt_file_path = 'sample_2.txt'  # 저장할 TXT 파일 경로

save_csv_as_txt(csv_file_path, txt_file_path)

def save_csv_as_txt(csv_file_path, txt_file_path):
    # CSV 파일을 DataFrame으로 불러오기
    df = pd.read_csv(csv_file_path)

    # TXT 파일로 변환하여 저장
    df.to_csv(txt_file_path, index=False, sep='\t')

input_json_path = 'reviews.json'
output_txt_path = 'data.txt'

# JSON 파일 읽기
data = pd.read_json(input_json_path)

# TXT 파일로 저장 (탭으로 구분)
data.to_csv(output_txt_path, sep='\t', index=False, encoding='utf-8')

# 사용 예시
csv_file_path = 'sample_1.csv'  # 읽어올 CSV 파일 경로
txt_file_path = 'sample_1.txt'  # 저장할 TXT 파일 경로

save_csv_as_txt(csv_file_path, txt_file_path)

if platform.system() == "Windows":
    plt.rcParams['font.family'] = "Malgun Gothic"
elif platform.system() == "Darwin":  # MacOS
    plt.rcParams['font.family'] = "AppleGothic"
else:  # Linux
    plt.rcParams['font.family'] = "NanumGothic"

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


text_lengths = [len(content) for content in df]

