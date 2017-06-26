# -*- coding: utf-8 -*-
# all the imports
import os
import traceback
import pickle
import ast
import re
from sklearn import datasets
from numpydoc.docscrape import NumpyDocString
import interfaceMl.extractSqlToPickle
from flask_restful import Resource, Api
from sklearn.utils.testing import all_estimators
from sklearn.model_selection import cross_val_score
from importlib import import_module
from flask import Flask, request, redirect, url_for, \
    render_template, flash, jsonify

# TODO change all UPLOAD_FOLDER by app.config get
with open('interfaceMl/DataSet/x_data_filtered.pickle', 'rb') as f:
    x_data_filtered = pickle.load(f)

with open('interfaceMl/DataSet/y_data_filtered.pickle', 'rb') as f:
    y_data_filtered = pickle.load(f)

# iris = datasets.load_iris()
# x_data_filtered, y_data_filtered = iris.data, iris.target
# dictEstimator is to stock object class and name objet
dictTypeEstimator = {}
dictEstimator = {}

# to store params estimator and name
dictParamEstimator = {}

# list object receive by post
listProcess = [
]



def getDicoParams(instanceClassifier):

    default_re = re.compile(r'\bdefault\s*[=:]\s*(?P<default>[^\)\b]+)')
    types_re = re.compile(r"(?P<type>(float|int(eger)?|str(ing)?|bool(ean)?|dict|))")

    type_map = {
        'string': str,
        'str': str,
        'boolean': bool,
        'bool': bool,
        'int': int,
        'integer': int,
        'float': float,
        'dict': dict,
    }
    doc = NumpyDocString("    " + instanceClassifier.__doc__)  # hack
    dico = {}
    for name2, type_, descriptions in doc['Parameters']:

        match = types_re.finditer(type_)
        types = (t.group('type') for t in match)

        types = [type_map.get(t, t) for t in types]

        match = default_re.search(type_)
        dico[name2] = types[0]
        # print(name, types, default)
    return dico


for name, class_ in all_estimators():
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
        dictParamEstimator[name] = dictEstimator[name]().get_params()

        # TODO CREATE DICT WITH PARAMS AND DESCRIPTION BY DOC
        dictTypeEstimator[name] = getDicoParams(dictEstimator[name])

class UseScikit2(Resource):
    def get(self):
        # return dictionnary {nameClassifier : {Params1:value1, Params2:value2}}
        print(dictTypeEstimator['SVC'])
        return jsonify(2)



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

                newValue = {}
                # TODO CONVERT DATA
                for nameparams, valueParams, in value.items():
                    print('params {0} type {1}'.format(valueParams, type(valueParams)))

                    # check if data diff to défault data
                    if valueParams == "":
                        print('value empty replaced by default')
                        newValue[nameparams] = dictParamEstimator[key][nameparams]
                    elif valueParams != dictParamEstimator[key][nameparams]:
                        print('value not empty and not equal to default. change type to type in docstring')
                        newValue[nameparams] = dictTypeEstimator[key][nameparams](valueParams)

                try:
                    # create the classificator
                    clf = dictEstimator[key]()
                    # send params issue by the request
                    clf.set_params(**newValue)

                    # évaluate the scoring
                    scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)

                    # Stock the result into variable resultat
                    resultat = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

                    # stock for the id of the shape, the result (dict form { idShape : resultat}
                    resultatform[k] = resultat

                except Exception:
                    traceback.format_exc()

        # return all result processed
        return jsonify(resultatform)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_UPLOAD']


def create_app():
    # create the application instance :)
    app = Flask(__name__)
    # load config from this file
    app.config.from_object(__name__)

    app.config.update(dict(
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='test',
        UPLOAD_FOLDER='interfaceMl/DataSet/',
        ALLOWED_EXTENSIONS_UPLOAD=set(['sqlite3']),
    ))

    api = Api(app)

    # route to process Scikit-learn
    api.add_resource(UseScikit, '/backend')
    # route to process Scikit-learn
    api.add_resource(UseScikit2, '/backend2')

    # define the route of the index
    @app.route('/')
    def test():
        return render_template('multipleAjaxTest.html')

    # define the route of the index
    @app.route('/index')
    def index():
        return render_template('index.html')

    # TODO create another route restful
    # define the route of the upload
    @app.route('/f', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            print(file)
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                print(os.path.abspath('.'))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "dbUpload.sqlite3"))
                interfaceMl.extractSqlToPickle.process()

                return redirect(url_for('index'))
        return render_template('upload.html')

    # Load default config and override config from an environment variable
    app.config.from_envvar('INTERFACEML_SETTINGS', silent=True)

    return app


# CHECK POST

# check SVM
# curl -i -H "Content-Type: application/json" -X POST -d '{"SVC": {"C": 1.0, "kernel": "rbf", "cache_size": 200, "tol": 0.001, "max_iter": -1, "class_weight": null, "shrinking": true, "degree": 3, "random_state": null, "coef0": 0.0, "decision_function_shape": null, "gamma": "auto", "probability": false, "verbose": false}}' http://localhost:5000/ScikitInfo

# check randomforest
# curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"RandomForestClassifier","Params":{"n_estimators":10},"Result":"None"}' http://localhost:5000/pokemon

# check gridsearch svm
# curl -i -H "Content-Type: application/json" -X POST -d '{"Clf":"SVM","GridSearch":"True", "ParamsGrid":[{"C": [1, 10, 100, 1000], "kernel": ["rbf"]}],"Result":"None"}' http://localhost:5000/index
