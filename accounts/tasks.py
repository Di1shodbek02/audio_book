from celery import shared_task
from django.core.mail import send_mail


@shared_task
def sent_email(email, title, price):
    send_mail(
        subject=title,
        from_email='From 127.0.0.1',
        recipient_list=[email],
        message=price,
        fail_silently=True
    )

    return 'Done'
