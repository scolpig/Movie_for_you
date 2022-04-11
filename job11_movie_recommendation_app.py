import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

form_window = uic.loadUiType('./mainWidget.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.df_reviews = pd.read_csv(
            './crawling_data/datasets/movie_review_2018_2022.csv')
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review01.mtx').tocsr()
        self.titles = list(self.df_reviews['title'])
        self.titles.sort()
        for title in self.titles:
            self.cmb_titles.addItem(title)
        self.cmb_titles.currentIndexChanged.connect(
            self.cmb_titles_slot)

    def cmb_titles_slot(self):
        title = self.cmb_titles.currentText()
        recommendation_titles = self.recommend_by_movie_title(title)
        self.lbl_recommend.setText(recommendation_titles)

    def recommend_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['title']==title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx],
                                   self.Tfidf_matrix)
        recommendation_titles = self.getRecommendation(cosine_sim)
        recommendation_titles = '\n'.join(list(recommendation_titles))
        return recommendation_titles


    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[1:11]
        movieidx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieidx]
        return recMovieList.iloc[:, 0]


app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())
