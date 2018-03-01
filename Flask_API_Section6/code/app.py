import sqlite3
from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT

from create_tables import init_db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items

init_db()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'superSecretKey'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create /auth endpoint

class Status_Check(Resource):
    def get(self):
        return {'message': 'Ok'}


api.add_resource(Status_Check, '/status')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
