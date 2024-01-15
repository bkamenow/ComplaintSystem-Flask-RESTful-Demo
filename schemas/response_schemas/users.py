from marshmallow import Schema, fields


class UserAuthResponseSchema(Schema):
    token = fields.String(required=True)
