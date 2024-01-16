from flask import request, abort

from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            schema = schema_name()
            data = request.get_json()
            errors = schema.validate(data)

            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)
        return wrapper
    return decorated_function


def permission_required(permission_role):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role == permission_role:
                return func(*args, **kwargs)
            raise Forbidden('You do not have permission to access this resource')
        return wrapper
    return decorated_function


def get_complaint_or_abort(obj, pk):
    complaint = obj.query.get(pk)
    if not complaint:
        abort(404, message=f"Complaint with ID {pk} not found")
    return complaint
