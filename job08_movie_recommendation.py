import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec

df_reviews = pd.read_csv('./crawling_data/datasets/movie_review_2018_2022.csv')
df_reviews.info()
def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    print(len(simScore))
    print(simScore)
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    simScore = simScore[1:11]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    return recMovieList.iloc[:, 0]

Tfidf_matrix = mmread('./models/Tfidf_movie_review01.mtx').tocsr()
with open('./models/tfidf01.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# # 영화 제목을 이용
# movie_idx = df_reviews[df_reviews['title']=='해피 데스데이 2 유'].index[0]
# print(movie_idx)
# 영화 index를 이용
# movie_idx = 566
# print(df_reviews.iloc[movie_idx, 0])

# key_word 이용
# embedding_model = Word2Vec.load('./models/word2vecModel.model')
# key_word = '성적'
# sim_word = embedding_model.wv.most_similar(key_word, topn=10)
# sentence = [key_word] * 11
# words = []
# for word, _ in sim_word:
#     words.append(word)
# for i, word in enumerate(words):
#     sentence += [word] * (10 - i)
#
# sentence = ' '.join(sentence)

# 문장을 이용
sentence = '적화통일돼서 배에서 기생충 키우고 싶나? 뭔 북한넘들 미화 영화가 이렇게 많냐. 배우들도 생각이 있으면 이런 영화는 걸러야하는 거 아니냐. 박정희, 전두환 군부 독재 시절을 미화하는 영화에 출연하면 무식해보이 듯이, 이런 북한 미화 영화 출연하는 것도 참으로 정신나간 듯이 보인다. 제목도 강철비가 뭐냐. 김영환 강철서신에서 가져온거냐. 정말 적당히 하자'
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)

print(recommendation)









