from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from accounts.models import User


class Category(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)


class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pics')
    rating = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Library(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    file = models.FileField(upload_to='file')


class Audio(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='audio')


class Subscription(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    start_data = models.DateTimeField()
    and_data = models.DateTimeField()
