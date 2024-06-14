from rest_framework.exceptions import APIException


class EmailServiceError(APIException):
    status_code = 500
    default_code = "unable_send_email"
