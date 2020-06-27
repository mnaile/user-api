from marshmallow import fields,validate
from extensions.extensions import ma
from app.model import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True, validate=[validate.Length(min=2,max=30)])
    surname = fields.String(required=True, validate=[validate.Length(min=2,max=40)])
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(min=8, max=100)])
    book_id = fields.Integer()

    class Meta:
        model = User
        load_instance = True

class UpdateSchema(ma.Schema):
    name = fields.String(validate=[validate.Length(min=2, max=30)])
    surname = fields.String(validate=[validate.Length(min=2, max=40)])
    email = fields.Email()
    password = fields.String(validate=[validate.Length(min=8, max=100)])
    book_id = fields.Integer()
