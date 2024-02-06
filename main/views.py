from django.core.cache import cache
from django.db import transaction
from django.http import Http404
from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Genre, Author, Book, File, Audio, Chapter, Review
from .serializer import CategorySerializer, GenreSerializer, UserPersonalizeSerializer, AuthorSerializer, \
    BookSerializerAll, ChapterSerializer, BookMarkSerializer, ReviewSerializer, RatingToReview, RatingForBookSerializer, \
    ReviewGetSerializer
from .utils import read_count


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

        # if request.user.id == bookmark_cache.get('user_id'):
        #     chapter_id = bookmark_cache.get('chapter_id')
        #     book_id = bookmark_cache.get('book_id')
        #     book = Book.objects.get(id=book_id)
        #     serialized = BookSerializerForChapter(book)
        #     # serialized.data['chapter'] = Chapter.objects.filter(book_id=book_id, id=chapter_id).values()
        #     serialized.data['file'] = File.objects.filter(chapter_id=chapter_id).values()
        #     serialized.data['audio'] = Author.objects.filter(chapter_id=chapter_id).values()

        # return Response({'success': True, 'book': serialized})

        read_count.delay(book_id)
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

        return Response({'succes': True})


class CategorySearch(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class BookSearch(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializerAll
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreSearch(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class AuthorSearch(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']


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
        book__data = Book.objects.filter()
        books = self.serializer_class(book__data, many=True)

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
