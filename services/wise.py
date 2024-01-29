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
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = self.main_url + "/v2/profiles"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        try:
            return resp.json()[0]['id']
        except (IndexError, KeyError):
            print(f"Error extracting profile ID. Response content: {resp.content}")
            raise InternalServerError("Unable to obtain profile ID")

    def create_quote(self, amount):
        url = self.main_url + "/v2/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "BGN",
            "targetAmount": amount,
            "profile": self.profile_id,
        }
        resp = requests.post(url, headers=self.headers, data=json.dumps(data))

        if resp.status_code == 200:
            resp = resp.json()
            return resp["id"]
        else:
            print(resp)
            raise InternalServerError("Payment provider is not available at the moment")

    def create_recipient(self, full_name, iban):
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

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"Recipient account creation failed. Response content: {resp.content}")
            raise err

        recipient_id = resp.json()["id"]
        return recipient_id

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())

        url = self.main_url + "/v1/transfers"
        body = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {
                "reference": "to my friend",
            },
        }

        resp = requests.post(url, headers=self.headers, json=body)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"Transfer creation failed. Response content: {resp.content}")
            raise err

        transfer_id = resp.json()["id"]
        return transfer_id

    def fund_transfer(self, transfer_id):
        url = self.main_url + f"/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        body = {"type": "BALANCE"}

        resp = requests.post(url, headers=self.headers, json=body)

        return resp

    def cancel_transfer(self, transfer_id):
        url = self.main_url + f"/v1/transfers/{transfer_id}/cancel"

        resp = requests.put(url, json={}, headers=self.headers)

        return resp


# if __name__ == "__main__":
#     wise_service = WiseService()
#     q_id = wise_service.create_quote(100)
#     recipient_id = wise_service.create_recipient('Bobi NEW', 'BG80BNBG96611020345678')
#     transfer = wise_service.create_transfer(recipient_id, q_id)
#     wise_service.cancel_transfer(52826943)
#
#     # print(q_id)
#     # print(recipient_id)
#     # print(transfer)
#     # print(fund_transfer)
