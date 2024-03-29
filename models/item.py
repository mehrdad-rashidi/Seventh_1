import sqlite3
from orm.db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Clolumn(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            # return cls(row[0], row[1])
            return cls(*row)

    def insert_item(self):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('seventh.sqlite')
        cursor = connection.cursor()
        query = "UPDATE items SET price =? WHERE name =?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
