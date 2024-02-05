from main.models import Book, File
from main.serializer import BookSerializerAll
from accounts.models import User
from main.models import Category
def get_file_and_audio_by_book_id(book: Book):
    file = File.objects.get(book_id=book.id)
    audio = File.objects.get(book_id=book.id)

    book = BookSerializerAll(book, audio=audio, file=file)

    return book


