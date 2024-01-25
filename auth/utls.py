import random
import string
from django.core.mail import send_mail
from django.conf import settings


def generate_verification_code(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for i in range(length))


def send_verification_code(email, code):
    subject = 'Verification Code'
    message = f'Your verification code is: {code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
