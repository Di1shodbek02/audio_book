from django.contrib import admin
from main.models import Genre, Book, Category, File, Author, Audio, Library, Subscription, Review, Chapter, Notification, \
    UserPersonalize, ViewCount, Rating


admin.site.register((Genre,ViewCount, Rating, Book, Category, Author, Library, Subscription, Review, Chapter, Notification, UserPersonalize))


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio', 'chapter_id', 'hashcode')
    exclude = ('hashcode',)


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'chapter_id', 'hashcode')
    exclude = ('hashcode',)

