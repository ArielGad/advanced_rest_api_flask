import traceback

from flask import make_response, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from flask_restful import Resource, request
from werkzeug.security import safe_str_cmp


from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from libs.mailgun import MailGunException


CREATED_SUCCESSFULLY = 'User created successfully, email was sent'
INVALID_CREDENTIALS = 'Invalid credentials'
SUCCESSFULLY_LOGGED_OUT = 'User <id={}> successfully logged out.'
USER_ALREADY_EXISTS = 'A user with username is already exists'
EMAIL_ALREADY_EXISTS = 'A user with email is already exists'
USER_DELETED = 'User deleted.'
USER_NOT_FOUND = 'User not found'
NOT_CONFIRMED_ERROR = 'You have not confirmed registration, please check your email <{}>'
USER_CONFIRMED = 'Confirmed'
FAILED_TO_CREATE = 'Internal server error'


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):

        # data = user_schema.load(request.get_json())  # THIS IS IN VANILA MARSHMALLOW
        user = user_schema.load(request.get_json())  # in flask_marshmallow, it is created a user model object

        if UserModel.find_by_username(user.username):
            return {'message': USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.username):
            return {'message': EMAIL_ALREADY_EXISTS}, 400

        try:
            user.save_to_db()
            user.send_confirmation_email()
            return {'message': CREATED_SUCCESSFULLY}, 201
        except MailGunException as e:
            user.delete_from_db()
            return {'message': str(e)}, 500
        except:
            traceback.print_exc()
            return {'message': FAILED_TO_CREATE}, 500


class User(Resource):
    @classmethod  # no need to use self here, so classmethod is fine
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message': USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json(), partial=('email', ))  # ignore email field if not present

        # find user in database
        user = UserModel.find_by_username(user_data.username)

        # check password and create tokens
        if user and safe_str_cmp(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200
            return {'message': NOT_CONFIRMED_ERROR.format(user.username)}
        return {'message': INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt().get('jti')  # jti is "JWT ID", a unique identifier for a JWT
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'message': SUCCESSFULLY_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)  # fresh=True means cred were just sent
        return {'access_token': new_token}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404

        user.activated = True
        user.save_to_db()
        headers = {'Content-Type': 'text/html'}  # by default the type is Json, and here we send HTML, so we need to declare it as text
        return make_response(render_template('confirmation_page.html', email=user.username), 200, headers)
