import os
import uuid

from werkzeug.exceptions import BadRequest

from constants import TEMP_FILES_PATH
from db import db
from managers.auth import auth
from models import Complaint, RoleType, State, TransactionModel
from services.s3 import S3Service
from services.wise import WiseService
from utils.helpers import decode_photo

s3_service = S3Service()


class ComplaintManager:
    @staticmethod
    def get_complaints():
        current_user = auth.current_user()
        role = current_user.role
        complaints = role_mapper[role]()

        return complaints

    @staticmethod
    def _get_complainer_complaints():
        current_user = auth.current_user()
        return Complaint.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def _get_approver_complaints():
        return Complaint.query.filter_by(status=State.pending).all()

    @staticmethod
    def _get_admin_complaints():
        return Complaint.query.filter_by().all()

    @staticmethod
    def create_complaint(complaint_data):
        current_user = auth.current_user()
        complaint_data['user_id'] = current_user.id

        photo_name = f"{str(uuid.uuid4())}.{complaint_data.pop('photo_extension')}"
        path_to_store_photo = os.path.join(TEMP_FILES_PATH, photo_name)
        photo_as_string = complaint_data.pop('photo')
        decode_photo(path_to_store_photo, photo_as_string)

        try:
            url = s3_service.upload_photo(path_to_store_photo, photo_name)
        except Exception as ex:
            raise Exception("Upload to s3 failed")
        finally:
            os.remove(path_to_store_photo)

        complaint_data["photo_url"] = url

        complaint = Complaint(**complaint_data)

        amount = complaint_data['amount']

        if int(amount) <= 0:
            raise BadRequest({'amount': ['Must be greater than or equal to 0.01.']})

        full_name = f'{current_user.first_name} {current_user.last_name}'
        iban = current_user.iban

        db.session.add(complaint)
        db.session.flush()

        ComplaintManager.issue_transaction(
            amount, full_name, iban, complaint.id
        )
        db.session.commit()
        return complaint

    @staticmethod
    def approve_complaint(complaint_id):
        ComplaintManager._validate_status(complaint_id)
        wise_service = WiseService()
        transfer = TransactionModel.query.filter_by(complaint_id=complaint_id).first()
        wise_service.fund_transfer(transfer.transfer_id)
        Complaint.query.filter_by(id=complaint_id).update({'status': State.approved})
        db.session.commit()

    @staticmethod
    def reject_complaint(complaint_id):
        ComplaintManager._validate_status(complaint_id)
        Complaint.query.filter_by(id=complaint_id).update({'status': State.rejected})
        db.session.commit()

    @staticmethod
    def _validate_status(complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if not complaint:
            raise BadRequest('Complaint with such id does not exist')

        if complaint.status != State.pending:
            raise BadRequest('Can not change status of  already processed complaints')

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id):
        wise_services = WiseService()
        quote_id = wise_services.create_quote(amount)

        recipient_id = wise_services.create_recipient(
            full_name,
            iban
        )

        transaction_id = wise_services.create_transfer(recipient_id, quote_id)
        transaction = TransactionModel(
            quote_id=quote_id,
            transfer_id=transaction_id,
            target_account_id=recipient_id,
            amount=amount,
            complaint_id=complaint_id,
        )

        return transaction


role_mapper = {
    RoleType.complainer: ComplaintManager._get_complainer_complaints,
    RoleType.approver: ComplaintManager._get_approver_complaints,
    RoleType.admin: ComplaintManager._get_admin_complaints,
}
