from flask_restful import Resource, reqparse
import sqlite3


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
