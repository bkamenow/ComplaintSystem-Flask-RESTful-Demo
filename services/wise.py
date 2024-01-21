import json
import uuid

import requests

from werkzeug.exceptions import InternalServerError
from decouple import config


class WiseService:
    def __init__(self):
        self.main_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
        }
        profile_id = self._get_profile_id()
        self.profile_id = profile_id
        print(profile_id)

    def _get_profile_id(self):
        url = self.main_url + "/v2/profiles"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        try:
            return resp.json()[0]['id']
        except (IndexError, KeyError):
            print(f"Error extracting profile ID. Response content: {resp.content}")
            raise

    def create_quote(self, amount):
        url = self.main_url + "/v3/quotes"
        body = {
            "sourceCurrency": "GBP",
            "targetCurrency": "USD",
            "sourceAmount": 200
        }

        resp = requests.post(url, headers=self.headers, json=body)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp.content)
            raise InternalServerError("Payment provider is not available at the moment")

    def create_recipient_account(self, full_name, iban):
        url = self.main_url + "/v1/accounts"
        body = {
            "currency": "BGN",
            "type": "iban",
            "profile": self.profile_id,
            "ownedByCustomer": False,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban,
            }
        }
        resp = requests.post(url, json=body, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        elif resp.status_code == 422:
            print(resp.content)  # Print response content for 422 Unprocessable Entity
        elif resp.status_code == 500:
            print(resp.content)  # Print response content for 500 Internal Server Error
            raise InternalServerError("Payment provider is not available at the moment")
        else:
            print(resp)
            raise InternalServerError("Unexpected error during recipient creation")

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())

        url = self.main_url + "/v1/transfers"
        body = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {},
        }

        resp = requests.post(url, headers=self.headers, json=body)

        if resp.status_code == 422:
            print("Error creating transfer. Response content:")
            print(resp.content)
        elif resp.status_code == 200:
            resp = resp.json()
            return resp
        else:
            print(resp)
            raise InternalServerError("Unexpected error during transfer creation")

        return resp

    def fund_transfer(self, transfer_id):
        url = self.main_url + f"/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        resp = requests.post(url, headers=self.headers)

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")


if __name__ == "__main__":
    wise_service = WiseService()
    q_id = wise_service.create_quote(100)
    recipient_id = wise_service.create_recipient_account('Bobi NEW', 'BG80BNBG96611020345678')
    transfer = wise_service.create_transfer(recipient_id, q_id)

    print(q_id)
    print(recipient_id)
    print(transfer)

