from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.userRegister import UserRegister
from resources.retrieveItem import Item
from resources.itemList import ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
if __name__ == '__main__':
    from orm.db import db
    db.inite_app(app)
    app.run(debug=True, port=5000)

# virtualenv venv --python=python3.11   --create virtual environment
# source venv/bin/activate
