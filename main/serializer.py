from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserInfo
from main.models import Category, Genre, Author, Book, Audio, File, Chapter, Review
from main.models import UserPersonalize


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


class ChapterSerializer(ModelSerializer):
    file = FileSerializerForChapter()
    audio = AudioSerializerForChapter()

    class Meta:
        model = Chapter
        # exclude = ('book_id',)
        fields = '__all__'


class BookSerializerForChapter(ModelSerializer):
    author = AuthorSerializer()
    chapter = ChapterSerializer()
    file = FileSerializerForChapter()
    audio = AudioSerializerForChapter()

    class Meta:
        model = Book
        fields = ('name', 'author', 'image', 'audio', 'file')


class BookMarkSerializer(serializers.Serializer): # noqa
    book_id = serializers.IntegerField()
    chapter_id = serializers.IntegerField()



class UserPersonalizeSerializer(ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = UserPersonalize
        exclude = ('id',)

class RatingToReview(serializers.Serializer): # noqa
    mark = serializers.IntegerField()
    review_id = serializers.IntegerField()



class RatingForBookSerializer(serializers.Serializer): # noqa
    mark = serializers.IntegerField()
    book_id = serializers.IntegerField()

