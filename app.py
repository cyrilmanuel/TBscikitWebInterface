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
        dictParamEstimator[name] = dictEstimator[name]().get_params(True)


class UseScikit(Resource):
    def get(self):
        return jsonify(dictParamEstimator)

    def post(self):

        # checker si les objets sont dans la liste et ne pas
        # faire de calcul si il y sont. juste retourner la réponse
        listProcess.clear()
        receive_json = request.get_json()
        resultatform = {}
        for k, v in receive_json.items():
            for key, value in v.items():
                clf = dictEstimator[key]()
                clf.set_params(**value)
                scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)
                resultat = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
                resultatform[k] = resultat
        return jsonify(resultatform)

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


if __name__ == '__main__':
    app.run(debug=True)
