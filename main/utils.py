from celery import shared_task
from django.db import transaction

from main.models import Book


@shared_task
def read_count(book_id):
    with transaction.atomic():
        book = Book.objects.select_for_update().get(pk=book_id)
        current_read_count = book.read_count
        book.view_count = current_read_count + 1
        book.save()

    return 'Done'



