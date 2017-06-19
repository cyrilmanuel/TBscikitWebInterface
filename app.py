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

        # recup the module name and path of scikit
        modulePath = str(class_).split("'")[1]

        # check if the name of the classifier is on the pass
        # if it is, change the module path to delete the name and the dot
        if name in modulePath:
            # remove name on module import
            dictEstimator[name] = getattr(import_module(modulePath.replace("." + name, '')), name)
        else:
            # great, let's push them
            dictEstimator[name] = getattr(import_module(modulePath), name)

        # stock the param of the classifier
        dictParamEstimator[name] = dictEstimator[name]().get_params(True)


class UseScikit(Resource):
    def get(self):
        # return dictionnary {nameClassifier : {Params1:value1, Params2:value2}}
        return jsonify(dictParamEstimator)

    def post(self):

        # checker si les objets sont dans la liste et ne pas
        # faire de calcul si il y sont. juste retourner la réponse
        listProcess.clear()
        receive_json = request.get_json()
        resultatform = {}
        for k, v in receive_json.items():
            for key, value in v.items():
                # TODO create try and if ok, return result
                # TODO and stock them into the listProcess
                # TODO if not, return into result, the error return by scikit

                # create the classificator
                clf = dictEstimator[key]()
                # send params issue by the request
                clf.set_params(**value)

                #évaluate the scoring
                # TODO créate an évaluation in fonction of the type
                # TODO of the CLF
                scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)

                # Stock the result into variable resultat
                resultat = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

                # stock for the id of the shape, the result (dict form { idShape : resultat}
                resultatform[k] = resultat

        # return all result processed
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

# define the route of the index
@app.route('/')
def hello_world():
    return render_template('index.html')


# start point
if __name__ == '__main__':
    app.run(debug=True)
