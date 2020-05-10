from marshmallow import pre_dump

from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):  # according to User model
    class Meta:
        model = UserModel
        load_only = ('password',)  # don't show pass while dump from OBJ to dict
        dump_only = ('id', 'activated')  # not mandatory, just declare that id is created in OBJ process, i.e. when loading there is no id

    @pre_dump
    def _pre_dump(self, user: UserModel):
        user.confirmation = [user.most_recent_confirmation]  # before dump, make user's confirmation property only a list of
        # recent confirmation
        return user





#  NOTE - the definitions below are related to original marshmallow pack

# from marshmallow import Schema, fields

# class UserSchema(Schema):  # according to User model
#     class Meta:
#         load_only = ('password',)  # don't show pass while dump from OBJ to dict
#         dump_only = ('id', )  # not mandatory, just declare that id is created in OBJ process,
#         # i.e. when loading there is no id
#     id = fields.Int()
#     username = fields.Str(required=True)
#     password = fields.Str(required=True)


