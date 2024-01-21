from flask import request
from flask_restful import Resource

from db import db
from managers.auth import auth
from managers.complaint import ComplaintManager
from models import RoleType, Complaint
from schemas.request_schemas.complaints import ComplaintRequestSchema
from schemas.response_schemas.complaints import ComplaintResponseSchema
from utils.decorators import validate_schema, permission_required, get_complaint_or_abort


class ComplaintsResource(Resource):
    @auth.login_required
    def get(self):
        complaints = ComplaintManager.get_complaints()
        return ComplaintResponseSchema(many=True).dump(complaints)

    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintRequestSchema)
    def post(self):
        data = request.get_json()
        complaint = ComplaintManager.create_complaint(data)

        return ComplaintResponseSchema().dump(complaint), 201


class ComplaintResource(Resource):
    @auth.login_required
    def get(self, pk):
        complaint = get_complaint_or_abort(Complaint, pk)

        complaint_schema = ComplaintResponseSchema()
        serialized_complaint = complaint_schema.dump(complaint)

        return serialized_complaint, 200

    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, pk):
        complaint = get_complaint_or_abort(Complaint, pk)

        db.session.delete(complaint)
        db.session.commit()

        return {"message": f"Complaint with ID {pk} has been deleted"}, 200

    @auth.login_required
    @validate_schema(ComplaintRequestSchema)
    @permission_required(RoleType.approver or RoleType.admin)
    def put(self, pk):
        pass
    # TODO


class ComplaintApproveResource(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def get(self, pk):
        ComplaintManager.approve_complaint(pk)


class ComplaintRejectResource(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def get(self, pk):
        ComplaintManager.reject_complaint(pk)
