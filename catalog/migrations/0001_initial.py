import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="Имя")),
                ("birth_year", models.PositiveIntegerField(blank=True, null=True, verbose_name="Год рождения")),
                ("country", models.CharField(blank=True, max_length=100, verbose_name="Страна")),
            ],
            options={"verbose_name": "Автор", "verbose_name_plural": "Авторы", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(unique=True, verbose_name="Слаг")),
            ],
            options={"verbose_name": "Жанр", "verbose_name_plural": "Жанры", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("published_year", models.PositiveIntegerField(verbose_name="Год издания")),
                ("pages", models.PositiveIntegerField(verbose_name="Страниц")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Цена")),
                ("rating", models.FloatField(default=0, verbose_name="Рейтинг (0–5)")),
                ("in_stock", models.BooleanField(default=True, verbose_name="В наличии")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Добавлена")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="books", to="catalog.author", verbose_name="Автор")),
                ("genre", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="books", to="catalog.genre", verbose_name="Жанр")),
            ],
            options={"verbose_name": "Книга", "verbose_name_plural": "Книги", "ordering": ["-rating", "title"]},
        ),
    ]
