from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

pokedex = [{'clf': 'SVM', 'params': {'C': 3}}
           ]

#
# root_parser = reqparse.RequestParser()
# root_parser.add_argument('id', type=int)
# root_parser.add_argument('name', type=str)
# root_parser.add_argument('nested_one', type=dict)
# root_parser.add_argument('nested_two', type=dict)
# root_args = root_parser.parse_args()
#
# nested_one_parser = reqparse.RequestParser()
# nested_one_parser.add_argument('id', type=int, location=('nested_one',))
# nested_one_args = nested_one_parser.parse_args(req=root_args)
#
# nested_two_parser = reqparse.RequestParser()
# nested_two_parser.add_argument('id', type=int, location=('nested_two',))
# nested_two_args = nested_two_parser.parse_args(req=root_args)

class Pokemon(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('clf', type=str, required=True, location='json', help='classifier not blank ! ')
        parser.add_argument('Params', type=dict, required=True, location='json', help='Value of params !')
        parser.add_argument('crossval', type=bool, location="json", help="not crossval score")

        args = parser.parse_args(strict=True)
        RecupClassificator = args['clf']
        RecupParamsClassificator = args['params']
        RecupIfCrossvalScore = args['crossval']
        # return the result
        return {'Result': 12}


api.add_resource(Pokemon, '/pokemon')

if __name__ == '__main__':
    app.run(debug=True)
