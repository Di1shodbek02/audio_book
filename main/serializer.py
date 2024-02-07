from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from accounts.serializers import UserInfo
from main.models import Category, Genre, Author, Book, Audio, File, Chapter, Review, Notification, Library


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class AudioSerializer(ModelSerializer):

    class Meta:
        model = Audio
        fields = '__all__'


class FileSerializer(ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'


class AudioSerializerForChapter(ModelSerializer):

    class Meta:
        model = Audio
        fields = ('audio',)


class FileSerializerForChapter(ModelSerializer):

    class Meta:
        model = File
        fields = ('file',)


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        exclude = ('mark_count', 'rating')


class ReviewGetSerializer(ModelSerializer):
    user_id = UserInfo()

    class Meta:
        model = Review
        fields = '__all__'


class BookSerializerAll(ModelSerializer):
    author_id = AuthorSerializer()
    genre = GenreSerializer(many=True)
    category_id = CategorySerializer()

    class Meta:
        model = Book
        fields = '__all__'


class NextBackChapterSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    chapter_number = serializers.IntegerField()


class ChapterSerializer(ModelSerializer):
    file = FileSerializerForChapter()
    audio = AudioSerializerForChapter()

    class Meta:
        model = Chapter
        # exclude = ('book_id',)
        fields = '__all__'


class AuthorForbook(ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name')


class BookSerializerForChapter(ModelSerializer):
    author_id = AuthorForbook()

    class Meta:
        model = Book
        fields = ('name', 'author_id', 'image')


class ChapterSerializerForBookmark(ModelSerializer):
    book_id = BookSerializerForChapter()
    file = FileSerializerForChapter()
    audio = AudioSerializerForChapter()

    class Meta:
        model = Chapter
        fields = '__all__'




class BookMarkSerializer(serializers.Serializer): # noqa
    book_id = serializers.IntegerField()
    chapter_id = serializers.IntegerField()


class RatingToReview(serializers.Serializer): # noqa
    mark = serializers.IntegerField()
    review_id = serializers.IntegerField()


class RatingForBookSerializer(serializers.Serializer): # noqa
    mark = serializers.IntegerField()
    book_id = serializers.IntegerField()


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class AddLibrarySerializer(serializers.Serializer):
    like = serializers.BooleanField()
    book_id = serializers.IntegerField()


class LibrarySerializer(ModelSerializer):

    class Meta:
        model = Library
        fields = ('book_id', 'user_id')



