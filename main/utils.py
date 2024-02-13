from celery import shared_task
from django.db import transaction

from main.models import Book, Notification
from main.models import File
from main.models import ViewCount


def get_file_and_audio_by_book_id(book: Book):
    file = File.objects.get(book_id=book.id)
    audio = File.objects.get(book_id=book.id)




@shared_task
def read_count(book_id):
    return 'Done'

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

