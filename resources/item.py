from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from flask_jwt_extended import fresh_jwt_required, jwt_required
from models.item import ItemModel


BLANK_ERROR = "'{}' cannot be blank"
ERROR_INSERTING = 'An error occurred inserting the item'
ITEM_DELETED = 'Item deleted'
ITEM_NOT_FOUND = 'Item not found'
NAME_ALREADY_EXISTS = 'An item with name {} already exists'


class Item(Resource):

    parser = reqparse.RequestParser()  # eliminate the option to change name field
    parser.add_argument('price', type=float, required=True, help=BLANK_ERROR.format('price'))
    parser.add_argument('store_id', type=int, required=True, help=BLANK_ERROR.format('store_id'))

    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}, 404

    @fresh_jwt_required
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name: str):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}, 200
        return {'message': ITEM_NOT_FOUND}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}, 200
