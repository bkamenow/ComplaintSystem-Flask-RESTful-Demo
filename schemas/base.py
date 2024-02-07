from marshmallow import Schema, fields


class UserRequestBase(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserResponseBase(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)


class ComplaintBase(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    amount = fields.Float(required=True)
