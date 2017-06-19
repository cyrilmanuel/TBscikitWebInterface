import pickle
from sklearn import svm
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


class WrapperScikit:
    dictClf = {}

    def __init__(self, recupCLF, recupParams, recupResult):
        self.recupCLF = recupCLF
        self.recupParams = recupParams
        self.recupResult = recupResult
        self.clf = None
        self.x_data_filtered = None
        self.y_data_filtered = None

        with open('../DataSet/x_data_filtered.pickle', 'rb') as f:
            self.x_data_filtered = pickle.load(f)

        with open('../DataSet/y_data_filtered.pickle', 'rb') as f:
            self.y_data_filtered = pickle.load(f)

    def createCLF(self):
        self.recupCLF


    def perimeter(self):
        return 2 * self.x + 2 * self.y

    def describe(self, text):
        self.description = text

    def authorName(self, text):
        self.author = text

    def scaleSize(self, scale):
        self.x = self.x * scale
        self.y = self.y * scale