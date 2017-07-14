# -*- coding: utf-8 -*-
# all the imports
import os
import pickle
import re
import traceback
from ast import literal_eval
from importlib import import_module
import matplotlib.pyplot as plt
from scikitplot import plotters as skplt
from numpydoc.docscrape import NumpyDocString
from flask import Flask, request, redirect, url_for, \
    render_template, flash, jsonify, send_file
from flask_restful import Resource, Api
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.utils.testing import all_estimators

# import others files in application.
import interfaceMl.extractSqlToPickle

with open('interfaceMl/DataSet/x_data_filtered.pickle', 'rb') as f:
    x_data_filtered = pickle.load(f)

with open('interfaceMl/DataSet/y_data_filtered.pickle', 'rb') as f:
    y_data_filtered = pickle.load(f)

dictDataToSendEstimator = {}
# dictEstimator for stocking object class and name objet
dictTypeEstimator = {}
dictEstimator = {}

# to store params estimator and name
dictParamEstimator = {}
dictDescriptionParam = {}

dictTypeEstimatorRegr = {}
dictEstimatorRegr = {}

# to store params estimator and name
dictParamEstimatorRegr = {}
dictDescriptionParamRegr = {}
# list object receive by post
listProcess = [
]


def getDicoParams(instanceClassifier):
    dico = {}
    types_re = re.compile(r"(?P<type>(float|int(eger)?|str(ing)?|bool(ean)?|dict?|list?|array?))")
    type_map = {
        'string': str,
        'str': str,
        'boolean': bool,
        'bool': bool,
        'int': int,
        'integer': int,
        'float': float,
        'dict': dict,
        'array': list,
        'list': list,
    }
    classifierTemp = instanceClassifier().get_params()
    doc = NumpyDocString("    " + instanceClassifier.__doc__)  # hack, get the doc for the classifier

    # For each params in get_params, take the name, first row contain type and the description
    for name, type_, descriptions in doc['Parameters']:
        # Find types in this row
        types = types_re.match(type_)
        # Check if the type was finded and if is not equal to "Infinity"
        if types != None and classifierTemp[name] != "Infinity":
            # Creates a complete description for this params
            if type_map.get(types.group()) == dict:
                completeDescription = str(type_) + "\n \n" + "Example : {'key':45} " + "\n \n" + " ".join(
                    str(e) for e in descriptions)
            elif type_map.get(types.group()) == list:
                completeDescription = str(type_) + "\n \n" + "Example : [value1,value2] " + "\n \n" + " ".join(
                    str(e) for e in descriptions)
            else:
                completeDescription = str(type_) + "\n \n" + " ".join(str(e) for e in descriptions)

            # add into the dict at the key (name of the params)
            # a tuple (instance of type, default value of params, description)
            dico[name] = (type_map.get(types.group()), classifierTemp[name], completeDescription)

    return dico


for name, class_ in all_estimators():
    # Retrieves the type of the current estimator
    typeclass = str(getattr(class_, "_estimator_type", None))

    # Delete the wrong estimator and check if it is a classifier
    if "_" not in name and typeclass == "classifier":

        # Retrieves the name and path of the module, from scikit for the current estimator
        modulePath = str(class_).split("'")[1]

        # Check if the classifier's name is in the path
        # If this is in, it is removed from the module path
        if name in modulePath:
            # Remove the name on the module path and stock an just-in-time import for the key (name of classifier)
            dictEstimator[name] = getattr(import_module(modulePath.replace("." + name, '')), name)
        else:
            # He not contain the name in the path, juste stock an just-in-time import for the key (name of classifier)
            dictEstimator[name] = getattr(import_module(modulePath), name)

        # Stock the dictionary that analyzes the doc.
        # It makes it possible to obtain the possible type of value of the classifier for each of these parameters
        dictTypeEstimator[name] = getDicoParams(dictEstimator[name])

        # stock the param of the classifier
        dictParamEstimator[name] = {key: v[1] for key, v in dictTypeEstimator[name].items()}
        dictDescriptionParam[name] = {key: v[2] for key, v in dictTypeEstimator[name].items()}

        # Delete the wrong estimator and check if it is a regressor
    elif "_" not in name and typeclass == "regressor" and name != "LassoLarsIC" and name != "RANSACRegressor":

        # Retrieves the name and path of the module, from scikit for the current estimator
        modulePath = str(class_).split("'")[1]

        # Check if the classifier's name is in the path
        # If this is in, it is removed from the module path
        if name in modulePath:
            # Remove the name on the module path and stock an just-in-time import for the key (name of classifier)
            dictEstimatorRegr[name] = getattr(import_module(modulePath.replace("." + name, '')), name)
        else:
            # He not contain the name in the path, juste stock an just-in-time import for the key (name of classifier)
            dictEstimatorRegr[name] = getattr(import_module(modulePath), name)

        dictTypeEstimatorRegr[name] = getDicoParams(dictEstimatorRegr[name])
        # stock the param of the classifier
        dictParamEstimatorRegr[name] = {key: v[1] for key, v in dictTypeEstimatorRegr[name].items()}
        dictDescriptionParamRegr[name] = {key: v[2] for key, v in dictTypeEstimatorRegr[name].items()}


def validationClassifier(dictParams, nameClassifier, typeOf):
    tabDict = []
    newValue = {}
    errorReturn = "\n"
    if (typeOf == "classifier"):
        tabDict.append(dictParamEstimator)
        tabDict.append(dictTypeEstimator)
    elif (typeOf == "regressor"):
        tabDict.append(dictParamEstimatorRegr)
        tabDict.append(dictTypeEstimatorRegr)

    for nameparams, valueParams, in dictParams.items():
        # best way to check if empty or blank.
        if type(valueParams) == str and not (valueParams and valueParams.strip()):
            newValue[nameparams] = tabDict[0][nameClassifier][nameparams]
            # in this state, valueParams = str and different to the default value of the params
        elif valueParams != tabDict[0][nameClassifier][nameparams]:
            # Check if bool. Convert them
            if tabDict[1][nameClassifier][nameparams][0] == bool:
                try:
                    valueConverted = literal_eval(valueParams.title())
                    newValue[nameparams] = tabDict[1][nameClassifier][nameparams][0](valueConverted)
                except Exception:
                    errorReturn += "Wrong parameter for {0} \n".format(nameparams)
            # Check if not bool and not str. Convert them
            elif tabDict[1][nameClassifier][nameparams][0] == dict:
                try:
                    valueConverted = literal_eval(valueParams)
                    newValue[nameparams] = tabDict[1][nameClassifier][nameparams][0](valueConverted)
                except Exception:
                    errorReturn += "Wrong parameter for {0} \n".format(nameparams)

            elif tabDict[1][nameClassifier][nameparams][0] != str:
                try:
                    valueConverted = literal_eval(valueParams)
                    newValue[nameparams] = tabDict[1][nameClassifier][nameparams][0](valueConverted)
                except Exception:
                    errorReturn += "Wrong parameter for {0} \n".format(nameparams)
    print('Erreur retourner : {0}'.format(errorReturn))
    return (newValue, errorReturn)


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

        for nameClassifier, dictParams in receive_json.items():
            if nameClassifier == 'ensemble Learning':
                estimators = []
                resultatFinal = ""
                for index, classifier, in dictParams.items():
                    for nameSubClass, dicoValueParams, in classifier.items():
                        typeOfClassifier = dicoValueParams.pop('typeOf', None)
                        resultValidation = validationClassifier(dicoValueParams, nameSubClass, typeOfClassifier)
                        newValue = resultValidation[0]
                        if type(resultValidation[1]) == str and not (resultValidation[1] and resultValidation[1].strip()):
                            clfChild = dictEstimator[nameSubClass]()
                            # send params issue by the request
                            clfChild.set_params(**newValue)

                            estimators.append((nameSubClass, clfChild))
                        else:
                            resultatFinal += "{0} in {1}.\n".format(resultValidation[1], nameSubClass)
                if type(resultatFinal) == str and not (resultatFinal and resultatFinal.strip()):
                    try:
                        clfEnsemble = VotingClassifier(estimators)
                        clfEnsemble.fit(x_data_filtered, y_data_filtered)
                        joblib.dump(clfEnsemble, 'interfaceMl/DataSet/newModel.pkl')

                    except Exception:
                        resultatFinal += traceback.format_exc()
                        # return all result processed

            else:
                typeOfClassifier = dictParams.pop('typeOf', None)
                resultValidation = validationClassifier(dictParams, nameClassifier, typeOfClassifier)
                newValue = resultValidation[0]
                resultatFinal = resultValidation[1]
                if type(resultatFinal) == str and not (resultatFinal and resultatFinal.strip()):
                    try:
                        if typeOfClassifier == "classifier":
                            # create the classificator
                            clf = dictEstimator[nameClassifier]()
                            # send params issue by the request
                            clf.set_params(**newValue)

                        elif typeOfClassifier == "regressor":
                            # create the classificator
                            clf = dictEstimatorRegr[nameClassifier]()
                            # send params issue by the request
                            clf.set_params(**newValue)
                            # évaluate the scoring

                        clf.fit(x_data_filtered, y_data_filtered)
                        joblib.dump(clf, 'interfaceMl/DataSet/newModel.pkl')

                    except Exception:
                        resultatFinal += traceback.format_exc()
                        # return all result processed

        receive_json[nameClassifier]['resultat'] = resultatFinal
        return jsonify(receive_json)


class UseScikit(Resource):
    def get(self):
        # return dictionnary {nameClassifier : {Params1:value1, Params2:value2}}
        # tab = [dictParamEstimator, dictDescriptionParam]
        data = {"regressor": [dictParamEstimatorRegr, dictDescriptionParamRegr],
                "classifier": [dictParamEstimator, dictDescriptionParam]}
        return jsonify(data)

    def post(self):
        # checker si les objets sont dans la liste et ne pas
        # faire de calcul si il y sont. juste retourner la réponse
        listProcess.clear()
        receive_json = request.get_json()
        resultatFinal = ""

        for nameClassifier, dictParams in receive_json.items():
            if nameClassifier == 'ensemble Learning':
                estimators = []
                for index, classifier, in dictParams.items():
                    for nameSubClass, dicoValueParams, in classifier.items():
                        typeOfClassifier = dicoValueParams.pop('typeOf', None)
                        resultValidation = validationClassifier(dicoValueParams, nameSubClass, typeOfClassifier)
                        newValue = resultValidation[0]


                        if type(resultValidation[1]) == str and not (resultValidation[1] and resultValidation[1].strip()):
                            clfChild = dictEstimator[nameSubClass]()
                            # send params issue by the request
                            clfChild.set_params(**newValue)

                            estimators.append((nameSubClass, clfChild))
                        else:
                            resultatFinal += "{0} in {1}.\n".format(resultValidation[1], nameSubClass)
                if type(resultatFinal) == str and not (resultatFinal and resultatFinal.strip()):
                    try:
                        clfEnsemble = VotingClassifier(estimators)

                        # évaluate the scoring
                        scores = cross_val_score(clfEnsemble, x_data_filtered, y_data_filtered, cv=3)

                        if typeOfClassifier == "classifier":

                            # Stock the result into variable resultat
                            resultatFinal = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

                        elif typeOfClassifier == "regressor":

                            # Stock the result into variable resultat
                            resultatFinal = ("Accuracy: %0.2f" % (scores.mean()))

                    except Exception:
                        resultatFinal += traceback.format_exc()
                        # return all result processed

            else:
                typeOfClassifier = dictParams.pop('typeOf', None)
                resultValidation = validationClassifier(dictParams, nameClassifier, typeOfClassifier)
                newValue = resultValidation[0]
                resultatFinal = resultValidation[1]
                if type(resultatFinal) == str and not (resultatFinal and resultatFinal.strip()):
                    try:
                        if typeOfClassifier == "classifier":
                            # create the classificator
                            clf = dictEstimator[nameClassifier]()
                            # send params issue by the request
                            clf.set_params(**newValue)
                            # évaluate the scoring
                            scores = cross_val_score(clf, x_data_filtered, y_data_filtered, cv=3)

                            # Stock the result into variable resultat
                            resultatFinal = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

                        elif typeOfClassifier == "regressor":
                            # create the classificator
                            clf = dictEstimatorRegr[nameClassifier]()
                            # send params issue by the request
                            clf.set_params(**newValue)
                            # évaluate the scoring
                            scores = cross_val_score(clf, x_data_filtered, y_data_filtered,
                                                     scoring='mean_squared_error',
                                                     cv=3)

                            # Stock the result into variable resultat
                            resultatFinal = ("Accuracy: %0.2f" % (scores.mean()))

                    except Exception:
                        resultatFinal += traceback.format_exc()
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
