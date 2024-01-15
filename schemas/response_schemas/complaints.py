from marshmallow import fields, Schema

from models import State
from schemas.base import ComplaintBase


class ComplaintResponseSchema(ComplaintBase):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    status = fields.Enum(State, by_value=True)
    user_id = fields.Integer(required=True)
    # TODO: nest user inside this schema


class ComplaintsResponseSchema(Schema):
    # TODO: make schema working with list of  Complaints schema
    complaints = fields.Nested(ComplaintResponseSchema, many=True)
