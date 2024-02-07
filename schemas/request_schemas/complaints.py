from marshmallow import fields

from schemas.base import ComplaintBase


class ComplaintRequestSchema(ComplaintBase):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)

