from django.urls import path

from main.views import CategoryRead, GenreReadAPIView, AuthorGetAll, GetBookAPIView, \
    ChapterDetailAPIView, GetChapters, BooksByNewRelease, BooksByTrendingNow, BooksBelongsToCategory, BookView, \
    BookmarkView, CategorySearch, BookSearch, GenreSearch, AuthorSearch

urlpatterns = [
    path('categories/', CategoryRead.as_view()),
    path('genres/', GenreReadAPIView.as_view()),
    path('authors/', AuthorGetAll.as_view()),
    path('books/', GetBookAPIView.as_view()),
    path('chapters/<int:book_id>/', GetChapters.as_view()),
    path('chapter-detail/<int:chapter_id>/', ChapterDetailAPIView.as_view()),
    path('new-release-books/', BooksByNewRelease.as_view()),
    path('trending-now-books/', BooksByTrendingNow.as_view()),
    path('books-by-category/<int:category_id>/', BooksBelongsToCategory.as_view()),
    path('book-detail/<int:book_id>/', BookView.as_view()),
    path('bookmark-button/', BookmarkView.as_view()),
    path('search-category', CategorySearch.as_view(), name='search-category'),
    path('search-book', BookSearch.as_view(), name='search-book'),
    path('search-genre', GenreSearch.as_view(), name='search-genre'),
    path('search-author', AuthorSearch.as_view(), name='search-author'),
]
