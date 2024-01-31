from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from main.models import Category, Genre, Author, Book, Audio, File, Chapter


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


class BookSerializerAll(ModelSerializer):
    author_id = AuthorSerializer()
    genre = GenreSerializer(many=True)
    category_id = CategorySerializer()

    class Meta:
        model = Book
        fields = '__all__'


class BookSerializerForChapter(ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ('name', 'author', 'image')


class ChapterSerializer(ModelSerializer):
    file = FileSerializerForChapter()
    audio = AudioSerializerForChapter()
    book = BookSerializerForChapter(read_only=True)

    class Meta:
        model = Chapter
        # exclude = ('book_id',)
        fields = '__all__'


class BookMarkSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    chapter_id = serializers.IntegerField()







