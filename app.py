from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import pickle
from sklearn import svm
import numpy as np
import sklearn
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV

app = Flask(__name__)
api = Api(app)

pokedex = [  # {'Clf': 'SVM', 'Params': {'C': 3}, 'Result': "None"}
]


class Pokemon(Resource):
    def get(self):
        return jsonify({'pokedex': pokedex})

    def post(self):

        pokedex.clear()

        with open('./DataSet/x_data_filtered.pickle', 'rb') as f:
            x_data_filtered = pickle.load(f)

        with open('./DataSet/y_data_filtered.pickle', 'rb') as f:
            y_data_filtered = pickle.load(f)

        parser = reqparse.RequestParser()
        parser.add_argument('Clf', type=str, required=True, location='json', help='classifier not blank ! ')
        parser.add_argument('ParamsClf', type=dict, required=False, location='json', help='Value of params !')
        parser.add_argument('GridSearch', type=bool, required=True, location='json', help="Gridsearch not defined !")
        parser.add_argument('ParamsGrid', type=dict, required=False, location='json', help='Value of params !')
        parser.add_argument('Result', type=str, required=True, location="json", help="not evaluator defined !")

        args = parser.parse_args(strict=True)

        dictClassificator = {
            'SVM': svm.SVC(),
            'Gaussian': GaussianNB(),
            'RandomForestClassifier': RandomForestClassifier(),
            'LogisticRegression': LogisticRegression(),
            'MLPClassifier': MLPClassifier(),
        }
        try:
            # create the classificator
            clf = dictClassificator[args['Clf']]

            # check if he want a gridsearch
            if args['GridSearch']:

                grid = GridSearchCV(estimator=clf, param_grid=[args['ParamsGrid']], n_jobs=-1)
                grid.fit(x_data_filtered, y_data_filtered)

                resultParams = ""
                for key, value in grid.best_params_.items():
                    resultParams+="param : {0}  value : {1} \n".format(key,value)

                args['Result'] = (
                    "Accuracy: {0}  \n ".format(grid.best_score_) + resultParams)

            else:
                # check if he have parameters
                if len(args['ParamsClf']) != 0:
                    clf.set_params(**args['ParamsClf'])

                # evaluate the scoring
                scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)
                args['Result'] = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

        except Exception as e:
            print(type(args['GridSearch']))
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)

            print(message)
            args['Result'] = message
            pass

        # return classificatior object in json
        classificator = {'Clf': args['Clf'], 'ParamsClf': args['ParamsClf'], 'GridSearch': args['GridSearch'],
                         'Result': args['Result']}
        pokedex.append(classificator)
        return jsonify({'pokedex': pokedex})

        # CHECK POST

        # check SVM
        # curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"SVM","Params":{"kernel":"rbf","C": 3},"Result":"None"}' http://localhost:5000/pokemon

        # check randomforest
        # curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"RandomForestClassifier","Params":{"n_estimators":10},"Result":"None"}' http://localhost:5000/pokemon

        # check gridsearch svm
        # curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"SVM","GridSearch":"True", "ParamsGrid":[{"C": [1, 10, 100, 1000], "kernel": ["rbf"]}],"Result":"None"}' http://localhost:5000/pokemon

api.add_resource(Pokemon, '/pokemon')

if __name__ == '__main__':
    app.run(debug=True)
