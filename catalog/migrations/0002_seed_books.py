"""Data-миграция: наполняет каталог тестовыми книгами, чтобы сразу было что показать."""
from decimal import Decimal

from django.db import migrations

GENRES = [
    ("Роман", "roman"),
    ("Фантастика", "fantastika"),
    ("Антиутопия", "antiutopiya"),
    ("Детектив", "detektiv"),
]

AUTHORS = [
    ("Михаил Булгаков", 1891, "Россия"),
    ("Фёдор Достоевский", 1821, "Россия"),
    ("Аркадий и Борис Стругацкие", None, "СССР"),
    ("Джордж Оруэлл", 1903, "Великобритания"),
    ("Агата Кристи", 1890, "Великобритания"),
    ("Рэй Брэдбери", 1920, "США"),
]

BOOKS = [
    # title, author, genre_slug, year, pages, price, rating, in_stock, description
    ("Мастер и Маргарита", "Михаил Булгаков", "roman", 1967, 480, "690.00", 4.9, True,
     "Роман о визите дьявола в Москву 1930-х, любви Мастера и Маргариты и истории Понтия Пилата, "
     "переплетённых в одно повествование о свободе, трусости и милосердии."),
    ("Преступление и наказание", "Фёдор Достоевский", "roman", 1866, 672, "540.50", 4.7, True,
     "История студента Раскольникова, решившегося на убийство ради проверки своей теории, "
     "и его мучительного пути к раскаянию."),
    ("Пикник на обочине", "Аркадий и Борис Стругацкие", "fantastika", 1972, 256, "420.00", 4.6, True,
     "Сталкер Рэдрик Шухарт проникает в Зону, оставленную инопланетянами, в поисках артефактов "
     "и легендарного Золотого шара, исполняющего желания."),
    ("1984", "Джордж Оруэлл", "antiutopiya", 1949, 328, "499.99", 4.8, False,
     "Уинстон Смит работает в Министерстве правды тоталитарного государства и решается на "
     "тихий бунт против Большого Брата."),
    ("Убийство в «Восточном экспрессе»", "Агата Кристи", "detektiv", 1934, 256, "380.00", 4.5, True,
     "Эркюль Пуаро расследует убийство в поезде, застрявшем в снегах, где у каждого пассажира "
     "есть алиби."),
    ("451 градус по Фаренгейту", "Рэй Брэдбери", "antiutopiya", 1953, 256, "1250.00", 4.4, True,
     "Пожарный Гай Монтэг сжигает книги, пока встреча с необычной девушкой не заставляет его "
     "усомниться во всём."),
    ("Трудно быть богом", "Аркадий и Борис Стругацкие", "fantastika", 1964, 224, "350.00", 3.2, True, ""),
]


def seed(apps, schema_editor):
    Author = apps.get_model("catalog", "Author")
    Genre = apps.get_model("catalog", "Genre")
    Book = apps.get_model("catalog", "Book")

    genres = {slug: Genre.objects.create(name=name, slug=slug) for name, slug in GENRES}
    authors = {
        name: Author.objects.create(name=name, birth_year=year, country=country)
        for name, year, country in AUTHORS
    }
    for title, author, genre, year, pages, price, rating, in_stock, descr in BOOKS:
        Book.objects.create(
            title=title, author=authors[author], genre=genres[genre],
            published_year=year, pages=pages, price=Decimal(price),
            rating=rating, in_stock=in_stock, description=descr,
        )


def unseed(apps, schema_editor):
    apps.get_model("catalog", "Book").objects.all().delete()
    apps.get_model("catalog", "Author").objects.all().delete()
    apps.get_model("catalog", "Genre").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
