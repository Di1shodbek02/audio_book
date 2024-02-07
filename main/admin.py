from django.contrib import admin
from main.models import Genre, Book, Category, File, Author, Audio, Library, Subscription, Review, Chapter, Notification, UserPersonalize


admin.site.register((Genre, Book, Category, File, Author, Audio, Library, Subscription, Review, Chapter, Notification, UserPersonalize))