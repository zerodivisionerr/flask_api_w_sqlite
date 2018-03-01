from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Items(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='A price must be specified in the form 11 or 11.11'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': '"{}" not found.'.format(name)}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': '"{}" is the name of an existing item.'.format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
            return item.json(), 201
        except:
            return {'message': 'Unable to insert item "{}"'.format(item.name)}, 500

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        try:
            item.save_to_db()
            return item.json(), 201
        except:
            return {'message': 'There was an error inserting '
                    'the item "{}"'.format(item.name)}, 500

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': 'There was no item named '
                    '"{}" to be deleted.'.format(name)}, 400
        try:
            item.delete_from_db()
        except:
            return {'message': 'An error occurred while attempting to '
                    'delete "{}"'.format(name)}, 500
        return {'message': '"{}" has been deleted.'.format(name)}
