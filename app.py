from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

# from security import authenticate, identity
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True  # So flask will see flask_jwt errors
app.secret_key = 'ariel'  # NOTE if I want to keep separate keys -> app.config['JWT_SECRET_KEY]

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # enable the blacklist for both tokens


api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# # JWT creates a new endpoint -> /auth
# jwt = JWT(app, authenticate, identity)

jwt = JWTManager(app)  # not creating /auth endpoint


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # Note that identity is declared as user.id in UserLogin(Resource)
    if identity == 1:  # Instead of hard-coding, need to read from config file or database
        return {'is_admin': 1}
    return {'is_admin': 0}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token.get('gti') in BLACKLIST  # identity defined in JWT


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an acess token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
