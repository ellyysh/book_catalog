from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField("Имя", max_length=150)
    birth_year = models.PositiveIntegerField("Год рождения", null=True, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Название", max_length=200)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="books", verbose_name="Жанр",
    )
    description = models.TextField("Описание", blank=True)
    published_year = models.PositiveIntegerField("Год издания")
    pages = models.PositiveIntegerField("Страниц")
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    rating = models.FloatField("Рейтинг (0–5)", default=0)
    in_stock = models.BooleanField("В наличии", default=True)
    created_at = models.DateTimeField("Добавлена", auto_now_add=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-rating", "title"]

    def __str__(self):
        return f"{self.title} ({self.author})"

    def get_absolute_url(self):
        return reverse("catalog:book_detail", args=[self.pk])
