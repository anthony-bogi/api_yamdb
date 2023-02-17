import random

from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile


def generate_confirmation_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_email_with_confirmation_code(data):
    username = data['username']
    addressee = [data['email'], ]
    sender = 'main@sender.pnt'
    subject = 'Письмо подтверждения.'
    confirmation_code = data['confirmation_code']
    message = (
        f'Привет, {username}! Данное письмо содержит код подтверждения.\n'
        f'Код: {confirmation_code}.\n'
        'Чтобы получить токен, отправьте запрос с полями:\n'
        'username и confirmation_code на .../api/v1/auth/token/.'
    )
    send_mail(subject, message, sender, addressee)

username_validator = RegexValidator(
    _lazy_re_compile(r'^[\w.@+-]+\Z'),
    message='Enter a valid username.',
    code='invalid',
)

def username_is_valid(username):
    try:
        username_validator(username)
        return True
    except ValidationError:
        return False
