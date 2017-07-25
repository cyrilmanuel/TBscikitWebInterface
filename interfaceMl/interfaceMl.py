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
from flask import Flask, request, render_template, jsonify, send_file
from flask_restful import Resource, Api
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn.utils.testing import all_estimators
from sklearn.datasets import load_iris
from mlxtend.regressor import StackingRegressor
from sklearn.svm import SVR

# import others files in application.
import interfaceMl.extractSqlToPickle

iris = load_iris()
x_data_filtered = iris.data
y_data_filtered = iris.target

def importData():
    """
    import data from file
    :return: nothing, modify the variable global
    """
    with open('interfaceMl/DataSet/x_data_filtered.pickle', 'rb') as f:
        global x_data_filtered
        x_data_filtered = pickle.load(f)

    with open('interfaceMl/DataSet/y_data_filtered.pickle', 'rb') as f:
        global y_data_filtered
        y_data_filtered = pickle.load(f)


# Dict store data for classificator
dictEstimator = {}
dictTypeEstimator = {}
dictParamEstimator = {}
dictDescriptionParam = {}

# Dict store data for regressor
dictTypeEstimatorRegr = {}
dictEstimatorRegr = {}
dictParamEstimatorRegr = {}
dictDescriptionParamRegr = {}

# list object receive by post
listProcess = [
]


def getDicoParams(instanceClassifier):
    """
    This function allows to retrieve the name of the parameter,
    the types for the accepted values ​​in case of modification and that description.

    :param instanceClassifier: the instance of the estimator issue by dictEstimator
    :return: A dictionary containing the name of the estimator as a key and a tuple
    as a value. The tuple contains (instance of type, default value of params, description)
    """
    dico = {}
    # regex to find type
    types_re = re.compile(r"(?P<type>(float|int(eger)?|str(ing)?|bool(ean)?|dict?|list?|array?))")

    # Map string to object
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


# ----------------------------------------------------------------------------------------------------------------
# ---------------------------------------- retrieves all estimators ----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------
# -------------------------------------- validation params estimators --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
def validationClassifier(dictParams, nameClassifier, typeOf):
    """
    This function makes it possible to check whether the value entered by the user and valid for each parameter
    of the estimator. If it is empty, it is replaced by the default value of the parameter.
    In the event of an error, an error message is returned indicating which parameter has an incorrect value.

    :param dictParams: dictionary of parameters for the estimator
    :param nameClassifier: the name of the estimator
    :param typeOf: define if the estimator is an classifier or regressor
    :return:
    """
    tabDict = []
    newValue = {}
    errorReturn = "\n"

    # define the dict to use for the validation.
    if (typeOf == "classifier"):
        tabDict.append(dictParamEstimator)
        tabDict.append(dictTypeEstimator)
    elif (typeOf == "regressor"):
        tabDict.append(dictParamEstimatorRegr)
        tabDict.append(dictTypeEstimatorRegr)

    # browse the dict params
    for nameparams, valueParams, in dictParams.items():
        # best way to check if empty or blank.
        if type(valueParams) == str and not (valueParams and valueParams.strip()):
            newValue[nameparams] = tabDict[0][nameClassifier][nameparams]
            # in this state, valueParams = str and different to the default value of the params
        elif valueParams != tabDict[0][nameClassifier][nameparams]:
            # Check if bool. Convert them
            if tabDict[1][nameClassifier][nameparams][0] == bool:
                try:
                    # Convert the value with AST and replace them on the dict
                    valueConverted = literal_eval(valueParams.title())
                    newValue[nameparams] = tabDict[1][nameClassifier][nameparams][0](valueConverted)
                except Exception:
                    errorReturn += "Wrong parameter for {0} \n".format(nameparams)

            # Check if is a Dict or list
            elif tabDict[1][nameClassifier][nameparams][0] == dict or tabDict[1][nameClassifier][nameparams][0] == list:
                try:
                    valueConverted = literal_eval(valueParams)
                    newValue[nameparams] = tabDict[1][nameClassifier][nameparams][0](valueConverted)
                except Exception:
                    errorReturn += "Wrong parameter for {0} \n".format(nameparams)

            # Check if is number because not list,dict,bool and string
            elif tabDict[1][nameClassifier][nameparams][0] != str:
                try:
                    valueConverted = literal_eval(valueParams)
                    newValue[nameparams] = tabDict[1][nameClassifier][nameparams][0](valueConverted)
                except Exception:
                    errorReturn += "Wrong parameter for {0} \n".format(nameparams)
    print('Erreur retourner : {0}'.format(errorReturn))
    return (newValue, errorReturn)

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

    def allowed_file(filename):
        """
        Checks if the file has a correct extension

        :param filename: name of the file
        :return: bool (true if has a correct extension)
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS_UPLOAD']

    # ----------------------------------------------------------------------------------------------------------------
    # ------------------------------------------ Routes REST IMPORTBDD -----------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------
    class ImportBDD(Resource):
        def post(self):
            # var contain error string
            result = ""
            if 'file' not in request.files:
                result += 'No file part in request \n'
            else:
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    result += 'No selected file \n'

                elif file and allowed_file(file.filename):
                    # print(os.path.abspath('.'))
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "dbUpload.sqlite3"))
                    try:
                        interfaceMl.extractSqlToPickle.process()
                        importData()
                    except Exception as e:
                        result += "extract data from BDD failed"
                else:
                    result = "Wrong file format !"
            return jsonify(result)

    # ----------------------------------------------------------------------------------------------------------------
    # -------------------------------------------- Routes REST PROCESS -----------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    class UseScikit(Resource):
        def get(self):
            data = {"regressor": [dictParamEstimatorRegr, dictDescriptionParamRegr],
                    "classifier": [dictParamEstimator, dictDescriptionParam]}
            return jsonify(data)

        def post(self):
            receive_json = request.get_json()
            resultatFinal = ""

            for nameClassifier, dictParams in receive_json.items():
                if nameClassifier == 'ensemble Learning':
                    estimators = []
                    for index, classifier, in dictParams.items():
                        for nameSubClass, dicoValueParams, in classifier.items():
                            #remove the type of
                            typeOfClassifier = dicoValueParams.pop('typeOf', None)
                            # validate all sub estimator
                            resultValidation = validationClassifier(dicoValueParams, nameSubClass, typeOfClassifier)
                            # Stores the validated dictionary
                            newValue = resultValidation[0]

                            # Test if no error occurred during validation
                            if type(resultValidation[1]) == str and not (
                                        resultValidation[1] and resultValidation[1].strip()):
                                # Create estimator by the type
                                if typeOfClassifier == "classifier":
                                    clfChild = dictEstimator[nameSubClass]()
                                elif typeOfClassifier == "regressor":
                                    clfChild = dictEstimatorRegr[nameSubClass]()

                                # send params issue by the request
                                clfChild.set_params(**newValue)

                                # add the estimator to the list
                                estimators.append((nameSubClass, clfChild))
                            # if error occurred durring validation return them on result var
                            else:
                                resultatFinal += "{0} in {1}.\n".format(resultValidation[1], nameSubClass)

                    # Test if no error for all sub estimator occurred during validation
                    if type(resultatFinal) == str and not (resultatFinal and resultatFinal.strip()):
                        try:
                            if typeOfClassifier == "classifier":
                                # Create an ensemble estimator type Voting
                                clfEnsemble = VotingClassifier(estimators)
                                # Stock the result into variable resultat
                                # Eval the scoring
                                scores = cross_val_score(clfEnsemble, x_data_filtered, y_data_filtered, cv=3)
                                resultatFinal = ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

                            elif typeOfClassifier == "regressor":

                                # Create an ensemble estimator type svr
                                svr_rbf = SVR(kernel='rbf')
                                clfEnsemble = StackingRegressor(regressors=[b for a, b in estimators],
                                                                meta_regressor=svr_rbf)
                                # évaluate the scoring
                                scores = cross_val_score(clfEnsemble, x_data_filtered, y_data_filtered, cv=3,
                                                         scoring='neg_mean_squared_error')
                                # Stock the result into variable resultat
                                resultatFinal = ("negatif mean squared error: %0.2f" % (scores.mean()))

                        except Exception:
                            # return all error scikit
                            resultatFinal += traceback.format_exc()


                else:
                    # extract the type of estimator
                    typeOfClassifier = dictParams.pop('typeOf', None)

                    #validation for all params
                    resultValidation = validationClassifier(dictParams, nameClassifier, typeOfClassifier)

                    # Stores the validated dictionary
                    newValue = resultValidation[0]

                    resultatFinal = resultValidation[1]

                    # Test if no error for all sub estimator occurred during validation
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
                                # create the Regressor
                                clf = dictEstimatorRegr[nameClassifier]()
                                # send params issue by the request
                                clf.set_params(**newValue)
                                # évaluate the scoring
                                scores = cross_val_score(clf, x_data_filtered, y_data_filtered,
                                                         scoring='neg_mean_squared_error',
                                                         cv=3)

                                # Stock the result into variable resultat
                                resultatFinal = ("negatif mean squared error: %0.2f" % (scores.mean()))

                        except Exception:
                            # return all error scikit
                            resultatFinal += traceback.format_exc()

            # add result to object base
            receive_json[nameClassifier]['resultat'] = resultatFinal

            # Return the object receive with the result
            return jsonify(receive_json)

    # ----------------------------------------------------------------------------------------------------------------
    # ----------------------------------------- Routes REST MODEL ----------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    class PickleFile(Resource):
        def get(self):
            return send_file('DataSet/newModel.pkl',
                             mimetype='application/python-pickle',
                             attachment_filename='newModel.pkl',
                             as_attachment=True)

        def post(self):
            receive_json = request.get_json()
            error = False
            try:
                for nameClassifier, dictParams in receive_json.items():
                    if nameClassifier == 'ensemble Learning':
                        estimators = []
                        typeOfClassifier = ""
                        resultatFinal = ""
                        for index, classifier, in dictParams.items():
                            for nameSubClass, dicoValueParams, in classifier.items():
                                typeOfClassifier = dicoValueParams.pop('typeOf', None)
                                resultValidation = validationClassifier(dicoValueParams, nameSubClass,
                                                                        typeOfClassifier)
                                newValue = resultValidation[0]
                                if type(resultValidation[1]) == str and not (
                                            resultValidation[1] and resultValidation[1].strip()):
                                    if typeOfClassifier == "classifier":
                                        clfChild = dictEstimator[nameSubClass]()
                                    elif typeOfClassifier == "regressor":
                                        clfChild = dictEstimatorRegr[nameSubClass]()
                                    # send params issue by the request
                                    clfChild.set_params(**newValue)

                                    estimators.append((nameSubClass, clfChild))
                                else:
                                    resultatFinal += "{0} in {1}.\n".format(resultValidation[1], nameSubClass)
                        if type(resultatFinal) == str and not (resultatFinal and resultatFinal.strip()):
                            try:
                                if (typeOfClassifier == "classifier"):
                                    clfEnsemble = VotingClassifier(estimators)
                                    clfEnsemble.fit(x_data_filtered, y_data_filtered)
                                elif (typeOfClassifier == "regressor"):

                                    est = [b for a, b in estimators]
                                    svr_rbf = SVR(kernel='rbf')
                                    clfEnsemble = StackingRegressor(regressors=est,
                                                                    meta_regressor=svr_rbf)
                                # évaluate the scoring
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
            except Exception as e:
                error = True
            return jsonify(error)

    # ----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------- Routes REST LEARNING CURVE ----------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    class LearningCurveImage(Resource):
        def get(self):
            return send_file('DataSet/learningCurve.png',
                             mimetype='image/png',
                             attachment_filename='learningCurve.png',
                             as_attachment=True)

        def post(self):
            receive_json = request.get_json()

            # get key and value of dictionnary. dont use for because he have one items on it
            idShape, nameAndParams = next(iter(receive_json['params'].items()))
            error = False
            try:
                for k, v in nameAndParams.items():
                    if (k != "ensemble Learning"):

                        # remove params because is add when process scikit and dont use here
                        v.pop('resultat', None)
                        try:
                            rf = dictEstimator[k]()
                        except:
                            rf = dictEstimatorRegr[k]()
                        rf.set_params(**v)
                        rf.fit(x_data_filtered, y_data_filtered)
                        skplt.plot_learning_curve(rf, x_data_filtered, y_data_filtered)
                        plt.title("Learning curve for {0} ID {1}".format(k, idShape))
                        plt.savefig('interfaceMl/DataSet/learningCurve.png')
                    else:
                        estimators = []
                        v.pop('resultat', None)
                        for i, j in v.items():
                            for e, fn in j.items():
                                try:
                                    clfChild = dictEstimator[e]()
                                except:
                                    clfChild = dictEstimatorRegr[e]()
                                # send params issue by the request
                                clfChild.set_params(**fn)
                                estimators.append((e, clfChild))
                                rf = VotingClassifier(estimators)
                                rf.fit(x_data_filtered, y_data_filtered)
                                # plot learning_curve
                                skplt.plot_learning_curve(rf, x_data_filtered, y_data_filtered)
                                plt.title("Learning curve for {0} ID {1}".format(k, idShape))
                                plt.savefig('interfaceMl/DataSet/learningCurve.png')
            except Exception as e:
                print(e)
                error = True
            return jsonify(error)

            # ----------------------------------------------------------------------------------------------------------------
            # ----------------------------------------- Routes and RESSOURCES ------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------------

    # route to process REST
    api.add_resource(ImportBDD, '/importbdd')
    api.add_resource(UseScikit, '/index/process')
    api.add_resource(PickleFile, '/index/model')
    api.add_resource(LearningCurveImage, '/index/learningcurve')

    #  Define the primary route for upload file
    @app.route('/')
    def upload_file():
        return render_template('upload.html')

    # Define route for one page with canvas
    @app.route('/index')
    def index():
        return render_template('index.html')

    # Load default config and override config from an environment variable
    app.config.from_envvar('INTERFACEML_SETTINGS', silent=True)

    return app
