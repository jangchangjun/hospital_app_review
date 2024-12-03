import MeCab
import pandas as pd

stop_word_list = ['병원', '예약', '진료', '접수']

def extract_noun(text):
    t =MeCab.Tagger()
    parsed = t.parse(text)
    nouns = []

    for line in parsed.split('\n'):
        if line == "EOS" or line =='':
            break
        word, features = line.split('\t')
        pos = features.split(',')[0]

        if pos == 'NNG' or pos == 'NNP':
            if len(word) >=2:
                if word not in stop_word_list:
                    nouns.append(word)
    return nouns

data_path = "ratings_result.txt"

dataset = pd.read_csv(data_path, sep = '\t').dropna(axis=0)

pos_text = list(dataset[dataset['label']==0]['content'].values)
neg_text = list(dataset[dataset['label']==1]['content'].values)

print(pos_text[:5])

processed_texts = [extract_noun(doc) for doc in neg_text]

print(processed_texts[:3])

from gensim import corpora
from gensim.models import LdaModel

dictionary = corpora.Dictionary(processed_texts)
print("전체 명사의 수 :",len(dictionary))

# above = 0.5~0.7사이
# 지나치게 일반적 단어 -> 불용어 처리
dictionary.filter_extremes(no_below=5, no_above=0.5)
print("전체 명사에 필터 적용한 개수 : ", len(dictionary))

# with open('dict_pos_text.txt', 'w', encoding='utf-8') as f:
#     for token, id in dictionary.token2id.items():
#         f.write(f'{token}\t{id}\n')

corpus = [dictionary.doc2bow(text) for text in processed_texts]
print(corpus[:3])

num_topics = 10

lda_model = LdaModel(
    corpus =corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=2024
)

for idx, topic in lda_model.print_topics(num_words = 10):
    print(f"토픽 #{idx+1} : {topic}")