from django.shortcuts import get_object_or_404, render

from .models import Book, Genre


def book_list(request, genre_slug=None):
    books = Book.objects.select_related("author", "genre")
    genre = None
    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        books = books.filter(genre=genre)
    return render(request, "catalog/book_list.html", {"books": books, "genre": genre})


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related("author", "genre"), pk=pk)
    return render(request, "catalog/book_detail.html", {"book": book})
