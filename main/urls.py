from django.urls import path

from main.views import CategoryRead, GenreReadAPIView, AuthorGetAll, GetBookAPIView, \
    ChapterDetailAPIView, GetChapters, BooksByNewRelease, BooksByTrendingNow, BooksBelongsToCategory, BookView, \
 \
    CreateUserPersonalize, BookmarkView, CategorySearch, BookSearch, GenreSearch, AuthorSearch, BooksByAuthorView, \
    BooksByGenreView, \
    ReviewCreateView, RatingToReviewView, RatingForBook, ReviewOfBookView

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
    path('search-category/', CategorySearch.as_view(), name='search-category'),
    path('user-personalize/', CreateUserPersonalize.as_view(), name='user-personalize'),
    path('search-category', CategorySearch.as_view(), name='search-category'),
    path('search-book', BookSearch.as_view(), name='search-book'),
    path('search-genre', GenreSearch.as_view(), name='search-genre'),
    path('search-author', AuthorSearch.as_view(), name='search-author'),
    path('book-by-author/<int:author_id>/', BooksByAuthorView.as_view()),
    path('book-by-genre/<int:genre_id>/', BooksByGenreView.as_view()),
    path('review-create/', ReviewCreateView.as_view(), name='review-create'),
    path('rating-for-review/', RatingToReviewView.as_view(), name='rating-review'),
    path('rating-for-book/', RatingForBook.as_view(), name='rating-review'),
    path('review-book/<int:book_id>/', ReviewOfBookView.as_view(), name='review-book')

]
