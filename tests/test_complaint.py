from models import RoleType
from tests.base import TestRESTAPIBase, generate_token
from tests.factories import UserFactory
from tests.helpers import encoded_photo


class TestComplaintSchema(TestRESTAPIBase):
    def test_required_fields_missing_raises(self):
        user = UserFactory(role=RoleType.complainer)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        data = {}
        res = self.client.post("/complaints", headers=headers, json=data)

        assert res.status_code == 400
        assert res.json == {
            "message": {
                "amount": ["Missing data for required field."],
                "description": ["Missing data for required field."],
                "photo_extension": ["Missing data for required field."],
                "photo": ["Missing data for required field."],
                "title": ["Missing data for required field."],
            }
        }

    def test_amount_is_zero_or_negative_raises(self):
        user = UserFactory(role=RoleType.complainer)
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        data = {
            "description": "test desc",
            "photo_extension": "jpg",
            "photo": encoded_photo,
            "title": "Test",
            "amount": -2
        }

        # Test with negative amount
        res = self.client.post("/complaints", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {
            "message": {"amount": ["Must be greater than or equal to 0.01."]}
        }

        # Test with negative amount
        data["amount"] = 0
        res = self.client.post("/complaints", headers=headers, json=data)
        assert res.status_code == 400
        assert res.json == {
            "message": {"amount": ["Must be greater than or equal to 0.01."]}
        }


