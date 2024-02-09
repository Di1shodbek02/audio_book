from django.urls import path

from main.views import CategoryRead, GenreReadAPIView, AuthorGetAll, GetBookAPIView, \
    ChapterDetailAPIView, GetChapters, BooksByNewRelease, BooksByTrendingNow, BooksBelongsToCategory, BookView, \
    CreateUserPersonalize, BookmarkView, CategorySearch, BookSearch, BooksByAuthorView, BooksByGenreView, \
    ReviewCreateView, RatingToReviewView, RatingForBook, ReviewOfBookView, NotificationAPIView, NotificationDetailView, \
    AddBookLibrary, RecommendedBooksView, RecommendedCategories, NextBackChapterDetail, PDFFileDownload, MP3FileDownload

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
    path('user-personalize/', CreateUserPersonalize.as_view(), name='user-personalize'),
    path('search-category', CategorySearch.as_view(), name='search-category'),
    path('search-book', BookSearch.as_view(), name='search-book'),
    path('book-by-author/<int:author_id>/', BooksByAuthorView.as_view()),
    path('book-by-genre/<int:genre_id>/', BooksByGenreView.as_view()),
    path('review-create/', ReviewCreateView.as_view(), name='review-create'),
    path('rating-for-review/', RatingToReviewView.as_view(), name='rating-review'),
    path('rating-for-book/', RatingForBook.as_view(), name='rating-review'),
    path('review-book/<int:book_id>/', ReviewOfBookView.as_view(), name='review-book'),
    path('notification/', NotificationAPIView.as_view(), name='notification'),
    path('notification-detail/<int:pk>', NotificationDetailView.as_view(), name='notification-detail'),
    path('book-dislike-like/', AddBookLibrary.as_view(), name='book-dislike-like'),
    path('recommended-book/', RecommendedBooksView.as_view(), name='recommended-books'),
    path('recommended-categories/', RecommendedCategories.as_view(), name='recommended-categories'),
    path('next-chapter-detail/<int:book_id>/<int:chapter_number>/<int:purpose>/', NextBackChapterDetail.as_view(), name='next-back-chapter-detail'),
    path('download-pdf/<str:hashcode>/', PDFFileDownload.as_view(), name='pdf_download'),
    path('download-mp3/<str:hashcode>/', MP3FileDownload.as_view(), name='mp3_download')

]
