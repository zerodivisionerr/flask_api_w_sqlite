from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from create_tables import init_db
from security import authenticate, identity
from user import UserRegister

init_db()

app = Flask(__name__)
app.secret_key = 'superSecretKey'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create /auth endpoint

items = []

class Status_Check(Resource):
    def get(self):
        return {'message': 'Ok'}

api.add_resource(Status_Check, '/status')

class Items(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}

api.add_resource(Items, '/items')

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='A price must be specified in the form 11 or 11.11'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            return item
        else:
            return {'message': '"{}" not found.'.format(name)}, 404


    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': '"{}" is already the name of an existing item.'.format(name)}, 400

        else:
            data = Item.parser.parse_args()
            item = {
            'name': name,
            'price': data['price']
            }
            items.append(item)
            return item, 201


    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item, 201

    @jwt_required
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item "{}" has been deleted.'.format(name)}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
