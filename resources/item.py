from flask_restful import Resource, request
# from flask_jwt import jwt_required
from flask_jwt_extended import fresh_jwt_required, jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema
from libs.strings import gettext


item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': gettext('item_not_found')}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):  # /item/chair -> I send
        if ItemModel.find_by_name(name):
            return {'message': gettext('store_name_exists').format(name)}, 400

        item_json = request.get_json()
        item_json['name'] = name  # price, store_id -> part of what I post

        item_data = item_schema.load(item_json)

        try:
            item_data.save_to_db()
        except:
            return {'message': gettext('item_error_inserting')}, 500

        return item_schema.dump(item_data), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': gettext('item_deleted')}, 200
        return {'message': gettext('item_not_found')}, 404

    @classmethod
    def put(cls, name):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json.get('price')
        else:
            item_json['name'] = name
            item = item_schema.load(item_json)

        item.save_to_db()
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': item_list_schema.dump(ItemModel.find_all())}, 200
