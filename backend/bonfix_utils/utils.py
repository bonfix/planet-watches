import string
import random

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import exception_handler
import logging;

logger = logging.getLogger(__name__)


# custom_exception_handler.py
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        errors = []
        message = response.data.get('detail')

        if not message:
            for field, value in response.data.items():
                errors.append("{} : {}".format(field, " ".join(value)))
            response.data = {'success': False, 'data': [], 'message': 'Validation Error',
                             'error': {'error_code': '', errors: errors}, "status_code": response.status_code}
        else:
            response.data = {'success': False, 'data': [], 'message': message,
                             'error': {'error_code': '', errors: [message]}, "status_code": response.status_code}

    return response


"""
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        resp_copy = response.data
        del response.data
        response.data = {}
        if (response.status_code == 400):
            response.data['code'] = 'ERR_UNAUTHORIZED'
            response.data['message'] = 'some errors occurred'
            response.data['extra'] = {}
            for key in resp_copy:
                response.data['extra'][key] = resp_copy[key]

    # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.data['status_code'] = response.status_code
    #     # response.data['FIXEEEEEEEER'] = response.status_code
    #     response.data['error'] = response.data.get('detail')
    #     del response.data['detail']

    return response
"""


def util_send_email(subject, recipient_list, plain_message, html_message=None):
    email_from = settings.EMAIL_HOST_USER
    res = 0
    if getattr(settings, 'SEND_ACTUAL_EMAIL', True):
        res = send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    logger.debug(f"Sent email: result:{res} subject:{subject} \n recipient_list:{recipient_list}\n"
                 f"message:{plain_message}")
    return res


def generate_random_string(size: int) -> str:
    result = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=size)
    )
    return result


