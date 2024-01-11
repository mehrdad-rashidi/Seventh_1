from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'massage': 'Item not found'}, 404

    def post(self, name):

        # if next(filter(lambda x: x['name'] == name, items), None):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name {} already exist.".format(name)}, 400
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = ItemModel(name, data['price'])
        # items.append(item)
        try:
            item.insert_item()
        except sqlite3.Error as e:
            return {"message": e.args}, 500
            # return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201


    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        connection = sqlite3.connect('identifier.sqlite')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name =?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            # items.append(item)
            try:
                updated_item.insert_item()
            except sqlite3.Error as err:
                return {"message": err.args}, 500

        else:
            try:
                updated_item.update_item()
            except sqlite3.Error as err:
                return {"message": err.args}, 500
        return item.json()
