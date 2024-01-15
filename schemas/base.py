from marshmallow import Schema, fields


class UserRequestBase(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class ComplaintBase(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    photo_url = fields.String(required=True)
    amount = fields.Float(required=True)