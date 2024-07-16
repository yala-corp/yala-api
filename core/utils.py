import json
import base64
import requests

from random import randint
from config.settings import SMS_MOBILE_API_URL, SMS_MOBILE_USERNAME, SMS_MOBILE_TOKEN
from core.templates import PHONE_VERIFICATION_CODE_MESSAGE


def generate_verification_code():
    return str(randint(100000, 999999))


def send_phone_verification(phone_number, verification_code):
    user_token = f"{SMS_MOBILE_USERNAME}:{SMS_MOBILE_TOKEN}"
    credentials = base64.b64encode(user_token.encode()).decode()

    payload = json.dumps(
        {
            "message": PHONE_VERIFICATION_CODE_MESSAGE.format(code=verification_code),
            "tpoa": "Yalatienes",
            "recipient": [
                {"msisdn": f"51{phone_number}"}
            ],
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic %s" % credentials,
        "Cache-Control": "no-cache",
    }

    response = requests.request(
        "POST", SMS_MOBILE_API_URL, headers=headers, data=payload
    )

    return response
