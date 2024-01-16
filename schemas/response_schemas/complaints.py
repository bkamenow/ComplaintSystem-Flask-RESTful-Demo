from marshmallow import fields, Schema

from models import State
from schemas.base import ComplaintBase, UserResponseBase


class ComplaintResponseSchema(ComplaintBase):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    status = fields.Enum(State, by_value=True)
    user_id = fields.Integer(required=True)
    # DONE TODO: nest user inside this schema
    user = fields.Nested(UserResponseBase(), only=("id", "first_name", "last_name", "email"))


class ComplaintsResponseSchema(Schema):
    # DONE TODO: make schema working with list of  Complaints schema
    complaints = fields.List(fields.Nested(ComplaintResponseSchema()), data_key='complaints')
