from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from django.contrib.auth.views import get_user_model

User = get_user_model()


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class UserPersonalize(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    personalize = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class UserPersonalizez_personalize(models.Model):
    user_personalize = models.ForeignKey(UserPersonalize, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        pass


class Genre(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    image = models.ImageField(upload_to='pics')
    created_at = models.DateTimeField(auto_now_add=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rating(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.mark)


class ViewCount(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book_id', 'user_id')


class Chapter(models.Model):
    chapter_number = models.IntegerField()
    name = models.CharField(max_length=200)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Library(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Book :' + self.book_id + '\n ' + 'User :' + self.user_id  # noqa


class Review(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField(default=0)
    mark_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class File(models.Model):
    chapter_id = models.OneToOneField(Chapter, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file')
    hashcode = models.CharField(max_length=64)


class Audio(models.Model):
    chapter_id = models.OneToOneField(Chapter, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='audio')
    hashcode = models.CharField(max_length=64)


class Subscription(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    start_data = models.DateTimeField()
    and_data = models.DateTimeField()


class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

