from flask_restful import Resource, request
# from flask_jwt import jwt_required
from flask_jwt_extended import fresh_jwt_required, jwt_required
from models.item import ItemModel
from marshmallow import ValidationError
from schemas.item import ItemSchema


ERROR_INSERTING = 'An error occurred inserting the item'
ITEM_DELETED = 'Item deleted'
ITEM_NOT_FOUND = 'Item not found'
NAME_ALREADY_EXISTS = 'An item with name {} already exists'

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):  # /item/chair -> I send
        if ItemModel.find_by_name(name):
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

        item_json = request.get_json()
        item_json['name'] = name  # price, store_id -> part of what I post

        try:
            item_data = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            item_data.save_to_db()
        except:
            return {'message': ERROR_INSERTING}, 500

        return item_schema.dump(item_data), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}, 200
        return {'message': ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json.get('price')
        else:
            item_json['name'] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.save_to_db()
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': item_list_schema.dump(ItemModel.find_all())}, 200
