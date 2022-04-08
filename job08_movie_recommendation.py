import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle

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

Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# # 영화 제목을 이용
# movie_idx = df_reviews[df_reviews['title']=='기생충'].index[0]
# print(movie_idx)
# 영화 index를 이용
movie_idx = 218
print(df_reviews.iloc[movie_idx, 0])
cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)









