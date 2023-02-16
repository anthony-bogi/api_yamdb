import random

from django.core.mail import send_mail


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
