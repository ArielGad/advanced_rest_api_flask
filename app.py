from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

# from security import authenticate, identity

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout, UserConfirm
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # So flask will see flask_jwt errors
app.secret_key = 'ariel'  # NOTE if I want to keep separate keys -> app.config['JWT_SECRET_KEY]

# app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # enable the blacklist for both tokens


api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

# # JWT creates a new endpoint -> /auth
# jwt = JWT(app, authenticate, identity)


jwt = JWTManager(app)  # not creating /auth endpoint


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(dycrypted_token):
    return dycrypted_token.get('jti') in BLACKLIST


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserConfirm, '/user_confirm/<int:user_id>')

if __name__ == '__main__':

    db.init_app(app)
    ma.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
