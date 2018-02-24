from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class Status_Check(Resource):
    def get(self):
        return {'message': 'Ok'}

api.add_resource(Status_Check, '/')

app.run(port=5000)

