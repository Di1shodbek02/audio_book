from celery import shared_task
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from main.models import Book, Notification, ViewCount
from main.serializer import AddViewCountSerializer


@shared_task
def view_count(book, user):
    if not ViewCount.objects.filter(book_id=book, user_id=user).exists():
        view_count_data = ViewCount.objects.create(book_id=book, user_id=user)
        view_count_data.save()

    return 'Task Completed'


@shared_task
def notification_status(pk):
    with transaction.atomic():
        notifi = Notification.objects.select_for_update().get(id=pk)
        notifi.status = True
        notifi.save()

    return 'Notification read'
