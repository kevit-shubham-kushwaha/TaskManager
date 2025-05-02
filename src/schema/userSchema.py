from marshmallow import Schema, fields, validate, post_load


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    user_role = fields.Str(required=True, validate=validate.OneOf(['admin', 'student']))


    # @post_load
    # def make_user(self, data, **kwargs):
    #     from src.models.user import User
    #     return User(**data)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))