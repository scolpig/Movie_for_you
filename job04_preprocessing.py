import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/movie_review_onesentence_2018_2022.csv')
print(df.head())
df.info()

stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords_list = list(stopwords['stopword'])
# cleaned_sentences = []
# for review in df.reviews:
#     review_word = review.split(' ')
#     words = []
#     for word in review_word:
#         if word not in stopwords_list:
#             words.append(word)
#     cleaned_sentence = ' '.join(words)
#     cleaned_sentences.append(cleaned_sentence)
# df['cleaned_sentences'] = cleaned_sentences
# df.to_csv('./crawling_data/cleaned_review_2018_2022.csv',
#           index=False)
# df.info()

okt = Okt()

cleaned_sentences = []
for sentence in df.reviews[3:8]:
    sentence = re.sub('[^가-힣]', '', sentence)
    token = okt.pos(sentence, stem=True)
    print(token)
    df_token = pd.DataFrame(token,  columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class']=='Noun') |
                                (df_token['class']=='Verb') |
                                (df_token['class']=='Adjective')]
    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1:
            if word not in stopwords_list:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    print(cleaned_sentence)
    cleaned_sentences.append(cleaned_sentence)
# df['cleaned_sentences'] = cleaned_sentences
# print(df.head())
# df.info()
# df.to_csv('./crawling_data/cleaned_review_2018_2022.csv',
#           index=False)











