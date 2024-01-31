import tarfile
from django.core.cache import cache
from rest_framework.generics import ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Genre, Author, Book, File, Audio, Chapter
from .serializer import CategorySerializer, GenreSerializer, \
    AuthorSerializer, BookSerializerAll, ChapterSerializer, BookSerializerForChapter, BookMarkSerializer


class CategoryRead(GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = Category.objects.all()
        serialized = self.serializer_class(categories, many=True)

        return Response({'success': True, 'categories': serialized.data})


class GenreReadAPIView(GenericAPIView):
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        genres = Genre.objects.all()
        serialized = self.serializer_class(genres, many=True)

        return Response({'success': True, 'genres': serialized.data})


class AuthorGetAll(GenericAPIView):
    serializer_class = AuthorSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        author = Author.objects.all()
        serialized = self.serializer_class(author, many=True)

        return Response({'data': serialized.data})


class GetBookAPIView(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        books = Book.objects.all()
        serialized = self.serializer_class(books, many=True)

        return Response({'books': serialized.data})


class BookView(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request, book_id):
        bookmark_cache = cache.get(request.user.id)
        if not request.user.id == bookmark_cache.get('user_id'):
            pass
        print(bookmark_cache)
        book__data = Book.objects.get(pk=book_id)
        book_data = self.serializer_class(book__data)

        return Response({'success': book_data.data})


class GetChapters(GenericAPIView):
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, book_id):
        chapters = Chapter.objects.filter(book_id=book_id)
        serialized = self.serializer_class(chapters, many=True)

        return Response({'chapters': serialized.data})


class ChapterDetailAPIView(GenericAPIView):
    serializer_class = ChapterSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, chapter_id):
        chapter = Chapter.objects.get(id=chapter_id)
        serialized = self.serializer_class(chapter)
        book_id = serialized.data.get('book_id')
        serialized.data['book'] = Book.objects.filter(id=int(book_id)).values()
        serialized.data['file'] = File.objects.filter(chapter_id=chapter_id).values()
        serialized.data['audio'] = Audio.objects.filter(chapter_id=chapter_id).values()

        return Response({'chapter': serialized.data})


class BooksByNewRelease(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        filtered_books = Book.objects.filter().order_by('-created_at')[:5]
        serialized_books = self.serializer_class(filtered_books, many=True)

        return Response({'new_release_books': serialized_books.data})


class BooksByTrendingNow(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        filtered_books = Book.objects.filter().order_by('-read_count')[:5]
        serialized_books = self.serializer_class(filtered_books, many=True)

        return Response({'trending_now_books': serialized_books.data})


class BooksBelongsToCategory(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self,request, category_id):
        filtered_books = Book.objects.filter(category_id=category_id)
        serialized_books = self.serializer_class(filtered_books, many=True)

        return Response({'books_by_category': serialized_books.data})


class BookmarkView(GenericAPIView):
    serializer_class = BookMarkSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user.id
        chapter_id = request.data.get('chapter_id')
        book_id = request.data.get('book_id')

        data = {
            'user_id': user,
            'chapter_id': chapter_id,
            'book_id': book_id
        }

        cache.set(user, data)

        return Response({'succes': True})