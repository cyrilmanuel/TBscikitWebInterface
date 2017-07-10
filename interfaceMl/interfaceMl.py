# -*- coding: utf-8 -*-
# all the imports
import base64
import os
import pickle
import re
import traceback
import matplotlib.pyplot as plt
from io import BytesIO
from ast import literal_eval
from importlib import import_module
from scikitplot import plotters as skplt
from flask import Flask, request, redirect, url_for, \
    render_template, flash, jsonify, send_file, make_response
from flask_restful import Resource, Api
from numpydoc.docscrape import NumpyDocString
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.utils.testing import all_estimators

import interfaceMl.extractSqlToPickle

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
dictDescriptionParam = {}
# list object receive by post
listProcess = [
]


def getDicoParams(instanceClassifier):
    dico = {}
    types_re = re.compile(r"(?P<type>(float|int(eger)?|str(ing)?|bool(ean)?))")
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
    temp = instanceClassifier().get_params()
    doc = NumpyDocString("    " + instanceClassifier.__doc__)  # hack
    for name, type_, descriptions in doc['Parameters']:
        types = types_re.match(type_)
        if types != None:
            completeDescription = str(type_) + "\n \n" + " ".join(str(e) for e in descriptions)
            dico[name] = (type_map.get(types.group()), temp[name], completeDescription)
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

        dictTypeEstimator[name] = getDicoParams(dictEstimator[name])
        # stock the param of the classifier
        dictParamEstimator[name] = {key: v[1] for key, v in dictTypeEstimator[name].items()}
        dictDescriptionParam[name] = {key: v[2] for key, v in dictTypeEstimator[name].items()}


class MatrixImage(Resource):
    def get(self):
        return send_file('DataSet/matrix.png',
                     mimetype='image/png',
                     attachment_filename='matrix.png',
                     as_attachment=True)

    def post(self):
        receive_json = request.get_json()
        for kdata, data in receive_json.items():
            for k, v in data.items():
                v.pop('resultat', None)
                rf = dictEstimator[k]()
                rf.set_params(**v)
                rf.fit(x_data_filtered, y_data_filtered)
                preds = rf.predict(x_data_filtered)
                skplt.plot_confusion_matrix(y_true=y_data_filtered, y_pred=preds)
                plt.title("Confusion Matrix for {0}".format(k))
                plt.savefig('interfaceMl/DataSet/matrix.png')
                return "OK"

class PickleFile(Resource):
    def get(self):
        return send_file('DataSet/newModel.pkl',
                         mimetype='application/python-pickle',
                         attachment_filename='newModel.pkl',
                         as_attachment=True)
    def post(self):
        receive_json = request.get_json()
        resultatf = {}
        print('-------------------- ---------------- ---------------------')
        print(receive_json)
        for nameClassifier, dictParams in receive_json.items():
            newValue = {}
            for nameparams, valueParams, in dictParams.items():
                # check if data diff to défault data
                print(valueParams)
                if valueParams == "":
                    print('value empty replaced by default')
                    newValue[nameparams] = dictParamEstimator[nameClassifier][nameparams]
                elif valueParams != dictParamEstimator[nameClassifier][nameparams]:
                    print('value not empty and not equal to default. change type to type in docstring')
                    # TODO verifie all type true false and int float sended by client
                    # TODO because he not work when params change in str convert by literal_eval.
                    # TODO change evaluation of the different params.
                    valueConverted = literal_eval(valueParams)
                    print('value convert ast = {0}'.format(valueConverted))
                    newValue[nameparams] = dictTypeEstimator[nameClassifier][nameparams][0](valueConverted)
                    print('valeur convert selons dico type= {0}'.format(newValue[nameparams]))
            try:
                # create the classificator
                clf = dictEstimator[nameClassifier]()
                # send params issue by the request
                clf.set_params(**newValue)

                clf.fit(x_data_filtered, y_data_filtered)
                joblib.dump(clf, 'interfaceMl/DataSet/newModel.pkl')

            except Exception:
                traceback.format_exc()
                # return all result processed
        return send_file('DataSet/newModel.pkl',
                         mimetype='application/python-pickle',
                         attachment_filename='newModel.pkl',
                         as_attachment=True)


class UseScikit(Resource):
    def get(self):
        # return dictionnary {nameClassifier : {Params1:value1, Params2:value2}}
        tab = [dictParamEstimator, dictDescriptionParam]
        return jsonify(tab)

    def post(self):
        # checker si les objets sont dans la liste et ne pas
        # faire de calcul si il y sont. juste retourner la réponse
        listProcess.clear()
        receive_json = request.get_json()
        resultatFinal = ""

        for nameClassifier, dictParams in receive_json.items():

            # TODO CHECK THE NAMECLASSIFIER IF ENSEMBLELEARNING DO THIS
            # TODO NEXT SUR ITEMS
            if (nameClassifier == 'ensemble Learning'):
                print("ENSEMBLE LEARNING")
                newValue = {}
                estimators = []
                for index, classifier, in dictParams.items():
                    for nameSubClass, valueParams, in classifier.items():
                        print(nameSubClass)
                        print("------------")
                        print(valueParams)

                        clfChild = dictEstimator[nameSubClass]()
                        # send params issue by the request
                        clfChild.set_params(**valueParams)

                        estimators.append((nameSubClass, clfChild))

                try:
                    clfEnsemble = VotingClassifier(estimators)
                    scoresEnsemble = cross_val_score(clfEnsemble, x_data_filtered, y_data_filtered, cv=3)
                    print(" in TRY")
                    resultatFinal = ("Accuracy: %0.2f (+/- %0.2f)" % (scoresEnsemble.mean(), scoresEnsemble.std() * 2))
                    print(("Accuracy: %0.2f (+/- %0.2f)" % (scoresEnsemble.mean(), scoresEnsemble.std() * 2)))
                    print("fin")
                except Exception:
                    resultatFinal = traceback.format_exc()
                    # return all result processed

            else:
                newValue = {}
                for nameparams, valueParams, in dictParams.items():
                    # check if data diff to défault data
                    print("params name : {0} value = ".format(nameparams))
                    print(valueParams)
                    # best way to check if empty or blank
                    if type(valueParams) == str and not (valueParams and valueParams.strip()):
                        print('value empty replaced by default')
                        newValue[nameparams] = dictParamEstimator[nameClassifier][nameparams]

                    elif valueParams != dictParamEstimator[nameClassifier][nameparams]:
                        # in this state, valueParams = str and different to the default value of the params
                        print('value not empty and not equal to default. change type to type in docstring')
                        if dictTypeEstimator[nameClassifier][nameparams][0] == bool:
                            valueParams = valueParams.title()

                        if dictTypeEstimator[nameClassifier][nameparams][0] != str:
                            valueConverted = literal_eval(valueParams)
                            print('value convert ast = {0}'.format(valueConverted))
                            newValue[nameparams] = dictTypeEstimator[nameClassifier][nameparams][0](valueConverted)
                            print('valeur convert selons dico type= {0}'.format(newValue[nameparams]))

                try:
                    # create the classificator
                    clf = dictEstimator[nameClassifier]()
                    # send params issue by the request
                    clf.set_params(**newValue)

                    # évaluate the scoring
                    scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)

                    # Stock the result into variable resultat
                    resultatFinal = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

                except Exception:
                    resultatFinal = traceback.format_exc()
                    # return all result processed
            receive_json[nameClassifier]['resultat'] = resultatFinal
        return jsonify(receive_json)


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
    api.add_resource(PickleFile, '/index/getfile')
    api.add_resource(MatrixImage, '/index/matrix')

    # define the route of the index
    @app.route('/index')
    def index():
        return render_template('index.html')

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_UPLOAD']

    # define the route of the upload
    @app.route('/', methods=['GET', 'POST'])
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
