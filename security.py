# from werkzeug.security import safe_str_cmp
# from models.user import UserModel
#
#
# def authenticate(username, password):
#     user = UserModel.find_by_username(username)
#     if user and safe_str_cmp(user.password, password):
#         return user
#
#
# def identity(payload):
#     user_id = payload['identity']
#     return UserModel.find_by_id(user_id)
#
#
#


# NOTE !!!

# This module is used for using flask_jwt
# from flask_jwt import JWT
# JWT creates a new endpoint -> /auth
# jwt = JWT(app, authenticate, identity) -> located in app.py
