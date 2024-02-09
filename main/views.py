import os

from django.core.cache import cache
from django.db import transaction
from django.http import FileResponse
from django.http import Http404
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Genre, Author, Book, File, Audio, Chapter, Review, Notification, Library, UserPersonalize
from .serializer import CategorySerializer, GenreSerializer, \
    AuthorSerializer, BookSerializerAll, ChapterSerializer, BookMarkSerializer, ReviewSerializer, RatingToReview, \
    RatingForBookSerializer, ReviewGetSerializer, NotificationSerializer, \
    LibrarySerializer, AddLibrarySerializer, ChapterSerializerForBookmark, \
    NextBackChapterSerializer
from .serializer import UserPersonalizeSerializer
from .utils import notification_status


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
        try:
            bookmark_cache = cache.get(request.user.id)
            if request.user.id == bookmark_cache.get('user_id'):
                chapter_id = bookmark_cache.get('chapter_id')
                book__id = bookmark_cache.get('book_id')
                if book_id == book__id:
                    chapter = Chapter.objects.get(id=chapter_id)
                    serialized = ChapterSerializerForBookmark(chapter)
                    serialized.data['book_id'] = Book.objects.filter(id=book__id).values()

                    return Response({'success': True, 'book': serialized.data})

        except Exception as e:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=book_id)
                current_read_count = book.read_count
                book.read_count = current_read_count + 1
                book.save()

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

    def get(self, request, category_id):
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

        cache.set(user, data, timeout=86400)

        return Response({'success': True})


class CategorySearch(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class BookSearch(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializerAll
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'genre__name', 'author_id__first_name', 'author_id__last_name', 'category_id__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_name = self.request.query_params.get('genre_name')
        if genre_name:
            queryset = queryset.filter(genre__name__icontains=genre_name)
        return queryset


class BooksByAuthorView(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request, author_id):
        book__data = Book.objects.filter(author_id=author_id)
        book_data = self.serializer_class(book__data, many=True)

        return Response({'book_by_author': book_data.data})


class BooksByGenreView(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request, genre_id):
        book_data = Book.objects.filter(genre=genre_id)
        books = self.serializer_class(book_data, many=True)

        return Response({'book_by_genre': books.data})

class ReviewCreateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def post(self, request):
        data = request.data
        data.update({'user_id': request.user.id})

        review = self.serializer_class(data=data)
        review.is_valid(raise_exception=True)
        review.save()

        return Response({'review': review.data})


class RatingToReviewView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingToReview

    def post(self, request):
        review_id = request.data.get('review_id')
        mark = request.data.get('mark')

        if 0 < mark < 6:

            try:
                with transaction.atomic():
                    review = Review.objects.select_for_update().get(pk=review_id)

                    current_rating = review.rating
                    current_mark_count = review.mark_count

                    if current_mark_count != 0:
                        review.rating = ((current_rating * current_mark_count) + mark) / (current_mark_count + 1)
                    else:
                        review.rating = mark
                    review.mark_count = current_mark_count + 1
                    review.save()

                return Response({'success': True})

            except Review.DoesNotExist:
                raise Http404("Review matching query does not exist.")

        raise Http404("Mark is incorrect")


class RatingForBook(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingForBookSerializer

    def post(self, request):
        book_id = request.data.get('book_id')
        mark = request.data.get('mark')

        if 0 < mark < 6:
            try:
                book = Book.objects.select_for_update().get(pk=book_id)

                current_rating = book.rating
                current_mark_count = book.count_rating

                if current_mark_count != 0:
                    book.rating = ((current_rating * current_mark_count) + mark) / (current_mark_count + 1)
                else:
                    book.rating = mark
                book.count_rating = current_mark_count + 1
                book.save()

            except Book.DoesNotExist:
                raise Http404('Book matching query does not exist')

        raise Http404('Mark is incorrect')


class ReviewOfBookView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewGetSerializer

    def get(self, request, book_id):
        review__data = Review.objects.filter(book_id=book_id)
        review = self.serializer_class(review__data, many=True)

        return Response({'review': review.data})


class CreateUserPersonalize(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPersonalizeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)  # noqa
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'user_personalize': serializer.data})


class NotificationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request):
        notification__data = Notification.objects.filter(user_id=request.user.id)
        notification = self.serializer_class(notification__data, many=True)

        return Response({'notifications': notification.data})


class NotificationDetailView(GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        notification_status.delay(pk)
        notification = Notification.objects.get(id=pk)
        serializer = self.serializer_class(notification)

        return Response({'notification': serializer.data})


class AddBookLibrary(GenericAPIView):
    serializer_class = AddLibrarySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        like = request.data.get('like')
        book_id = request.data.get('book_id')
        user_id = request.user.id
        if like:
            if Library.objects.filter(book_id=book_id, user_id=user_id).exists():
                raise Exception({'detail': 'You already have such book'})
            data = {
                'book_id': book_id,
                'user_id': user_id
            }
            library = LibrarySerializer(data=data)
            library.is_valid(raise_exception=True)
            library.save()

            return Response({'message': 'Book Added Successfully'})

        if not Library.objects.filter(book_id=book_id, user_id=user_id).exists():
            raise Exception({'detail': 'Such Book Not Found in Your Library'})

        library = Library.objects.get(book_id=book_id, user_id=user_id)
        library.delete()

        return Response({'message': 'Book Removed Successfully'})


class RecommendedBooksView(GenericAPIView):
    serializer_class = BookSerializerAll
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        book__data = Book.objects.filter().order_by('-created_at')
        book = self.serializer_class(book__data, many=True)
        return Response({'books': book.data})


class RecommendedCategories(GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        categories = UserPersonalize.objects.get(user_id=request.user).personalize.all()
        category = self.serializer_class(categories, many=True)

        return Response({'categories': category.data})


class NextBackChapterDetail(GenericAPIView):
    serializer_class = NextBackChapterSerializer
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, book_id, chapter_number, purpose):
        if not purpose:
            purpose = -1

        try:
            chapter = Chapter.objects.get(book_id=book_id, chapter_number=chapter_number + purpose)
            chapter_serializer = ChapterSerializer(chapter)
            chapter_serializer.data['file'] = File.objects.filter(chapter_id=chapter.id).values()
            chapter_serializer.data['audio'] = Audio.objects.filter(chapter_id=chapter.id).values()

            return Response({'chapter': chapter_serializer.data})
        except Exception as e:
            return Response({'detail': "Not Found Such Chapter"})

class PDFFileDownload(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, hashcode):
        try:
            file_instance = File.objects.get(hashcode=hashcode)
        except File.DoesNotExist:
            return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        file_path = file_instance.file.path
        file_name = os.path.basename(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


class MP3FileDownload(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, hashcode):
        try:
            audio_instance = Audio.objects.get(hashcode=hashcode)
        except Audio.DoesNotExist:
            return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        file_path = audio_instance.audio.path
        file_name = os.path.basename(file_path)
        response = FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
