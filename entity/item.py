from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        item = self.find_by_name(name)
        if item:
            return item
        return {'massage': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):

        # if next(filter(lambda x: x['name'] == name, items), None):
        if self.find_by_name(name):
            return {'message': "An item with name {} already exist.".format(name)}, 400
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = {'name': name, 'price': data['price']}
        # items.append(item)
        try:
            self.insert_item(item)
        except sqlite3.Error as e:
            return {"message": e.args}, 500
            # return {"message": "An error occurred inserting the item."}, 500
        return item, 201

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

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
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            # items.append(item)
            try:
                self.insert_item(updated_item)
            except sqlite3.Error as err:
                return {"message": err.args}, 500

        else:
            try:
                self.update_item(updated_item)
            except sqlite3.Error as err:
                return {"message": err.args}, 500
        return item

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()

        query = "UPDATE items SET price =? WHERE name =?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()
