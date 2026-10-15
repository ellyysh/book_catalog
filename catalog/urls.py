from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("genre/<slug:genre_slug>/", views.book_list, name="books_by_genre"),
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
]
