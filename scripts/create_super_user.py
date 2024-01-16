from werkzeug.security import generate_password_hash

from db import db
from app import app
from models import User, RoleType


def create_superuser(first_name, last_name, email, password, phone):
    password_hash = generate_password_hash(password)

    with app.app_context():
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password_hash,
            role=RoleType.admin,
            phone=phone
        )

        db.session.add(user)
        db.session.commit()

    print('Superuser created successfully.')


if __name__ == '__main__':
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    phone = input("Enter phone number: ")

    create_superuser(first_name, last_name, email, password, phone)
