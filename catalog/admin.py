from django.contrib import admin

from .models import Author, Book, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_year", "country")
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "published_year", "price", "rating", "in_stock")
    list_filter = ("genre", "in_stock")
    search_fields = ("title", "author__name")
