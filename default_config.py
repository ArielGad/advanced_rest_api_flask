"""This is for development"""

import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # did not use get() intentionally, so that if there is not env variable, the code will crash
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens

UPLOADED_IMAGES_DEST = os.path.join("static", "images")  # manage root folder

