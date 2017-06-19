from flask import Flask, jsonify, render_template, json, request
from flask_restful import Resource, Api, reqparse
import pickle
from sklearn.utils.testing import all_estimators
from sklearn.model_selection import cross_val_score, GridSearchCV
from importlib import import_module

app = Flask(__name__)
api = Api(app)

with open('./DataSet/x_data_filtered.pickle', 'rb') as f:
    x_data_filtered = pickle.load(f)

with open('./DataSet/y_data_filtered.pickle', 'rb') as f:
    y_data_filtered = pickle.load(f)

# create liste with estimator and the params
# dictEstimator is to stock object class and name objet
dictEstimator = {}

# to store params estimator and name
dictParamEstimator = {}

# list object receive by post
listProcess = [
]

for name, class_ in all_estimators():

    # prin if is a classifier, a regression or none
    # print(getattr(class_, "_estimator_type", None))

    if "_" not in name and str(getattr(class_, "_estimator_type", None)) == "classifier":
        modulePath = str(class_).split("'")[1]
        if name in modulePath:
            # remove name on module import
            dictEstimator[name] = getattr(import_module(modulePath.replace("." + name, '')), name)
        else:
            dictEstimator[name] = getattr(import_module(modulePath), name)

        # stock get params
        dictParamEstimator[name] = dictEstimator[name]().get_params(False)


class UseScikit(Resource):
    def get(self):
        return jsonify(dictParamEstimator)
    def post(self):
        listProcess.clear()
        receive_json = request.get_json()
        for key, value in receive_json.items():
            clf = dictEstimator[key]()
            clf.set_params(**value)
            scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)
            resultat = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        return jsonify(resultat)
        # parser = reqparse.RequestParser()
        # parser.add_argument('Clf', type=str, required=True, location='json', help='classifier not blank ! ')
        # parser.add_argument('ParamsClf', type=dict, required=False, location='json', help='Value of params !')
        # parser.add_argument('GridSearch', type=int, required=True, location='json', help='Gridsearch not defined !')
        # parser.add_argument('ParamsGrid', type=dict, required=False, location='json', help='Value of params !')
        # parser.add_argument('Result', type=str, required=True, location='json', help='not evaluator defined !')
        #
        # args = parser.parse_args()
        #
        # dictClassificator = {
        #     'SVM': svm.SVC(),
        #     'Gaussian': GaussianNB(),
        #     'RandomForestClassifier': RandomForestClassifier(),
        #     'LogisticRegression': LogisticRegression(),
        #     'MLPClassifier': MLPClassifier(),
        # }
        # try:
        #     # create the classificator
        #     clf = dictClassificator[args['Clf']]
        #
        #     # check if he want a gridsearch
        #     if args['GridSearch'] == 1:
        #
        #         args['ParamsGrid'] = {"C": [1, 10, 100, 1000], "kernel": ["rbf"]}
        #         grid = GridSearchCV(estimator=clf, param_grid=[args['ParamsGrid']], n_jobs=-1)
        #         grid.fit(x_data_filtered, y_data_filtered)
        #
        #         resultParams = ""
        #         for key, value in grid.best_params_.items():
        #             resultParams += "param : {0}  value : {1} \n ".format(key, value)
        #
        #         args['Result'] = (
        #             "Accuracy: {0}  \n ".format(grid.best_score_) + resultParams)
        #
        #     else:
        #         # check if he have parameters
        #         if len(args['ParamsClf']) != 0:
        #             clf.set_params(**args['ParamsClf'])
        #
        #         # evaluate the scoring
        #         scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)
        #         args['Result'] = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        #
        # except Exception as e:
        #     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        #     message = template.format(type(e).__name__, e.args)
        #
        #     print(message)
        #     args['Result'] = message
        #     pass
        #
        # # return classificatior object in json
        # classificator = {'Clf': args['Clf'], 'ParamsClf': args['ParamsClf'], 'GridSearch': args['GridSearch'],
        #                  'Result': args['Result']}
        # listProcess.append(classificator)
        #
        # return jsonify({'listProcess': listProcess})

        # CHECK POST

        # check SVM
        # curl -i -H "Content-Type: application/json" -X POST -d '{"SVC": {"C": 1.0, "kernel": "rbf", "cache_size": 200, "tol": 0.001, "max_iter": -1, "class_weight": null, "shrinking": true, "degree": 3, "random_state": null, "coef0": 0.0, "decision_function_shape": null, "gamma": "auto", "probability": false, "verbose": false}}' http://localhost:5000/ScikitInfo

        # check randomforest
        # curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"RandomForestClassifier","Params":{"n_estimators":10},"Result":"None"}' http://localhost:5000/pokemon

        # check gridsearch svm
        # curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"SVM","GridSearch":"True", "ParamsGrid":[{"C": [1, 10, 100, 1000], "kernel": ["rbf"]}],"Result":"None"}' http://localhost:5000/index


# route to process Scikit-learn
api.add_resource(UseScikit, '/backend')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/nice')
def hello_world2():
    return render_template('tutoAjaxJquery.html')


if __name__ == '__main__':
    app.run(debug=True)
