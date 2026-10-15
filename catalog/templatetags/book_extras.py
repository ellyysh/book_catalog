"""Кастомные шаблонные фильтры и теги каталога книг.

Подключение в шаблоне:  {% load book_extras %}

Фильтры:
    rub            — 1250.5   -> «1 250,50 ₽»
    stars          — 4.6      -> «★★★★★» (рейтинг звёздами, округление до целого)
    reading_time   — 480      -> «≈ 16 ч чтения» (страницы -> время)
    ru_plural      — 5|ru_plural:"книга,книги,книг" -> «книг»
    book_age       — 1967     -> «59 лет назад»

Теги:
    {% total_books %}                — simple_tag: число книг в базе
    {% avg_price as var %}           — simple_tag: средняя цена (можно сохранить в переменную)
    {% genre_menu active_slug %}     — inclusion_tag: меню жанров (шаблон includes/genre_menu.html)
    {% current_year %}               — simple_tag: текущий год
"""
import datetime
from decimal import Decimal, InvalidOperation

from django import template
from django.db.models import Avg, Count

from catalog.models import Book, Genre

register = template.Library()


# ---------- Фильтры ----------

@register.filter
def rub(value):
    """Форматирует число как цену в рублях: пробел-разделитель тысяч, запятая, знак ₽."""
    try:
        amount = Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return value
    text = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
    return f"{text} ₽"


@register.filter
def stars(value, max_stars=5):
    """Превращает рейтинг в строку из закрашенных и пустых звёзд."""
    try:
        full = round(float(value))
        max_stars = int(max_stars)
    except (TypeError, ValueError):
        return ""
    full = max(0, min(full, max_stars))
    return "★" * full + "☆" * (max_stars - full)


@register.filter
def ru_plural(number, forms):
    """Русское склонение по числу. Пример: {{ n }} {{ n|ru_plural:"книга,книги,книг" }}"""
    try:
        n = abs(int(number))
    except (TypeError, ValueError):
        return ""
    one, few, many = [f.strip() for f in forms.split(",")]
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


@register.filter
def reading_time(pages, pages_per_hour=30):
    """Оценка времени чтения по количеству страниц (≈30 стр./час)."""
    try:
        minutes = int(pages) * 60 // int(pages_per_hour)
    except (TypeError, ValueError, ZeroDivisionError):
        return ""
    if minutes < 60:
        return f"≈ {minutes} мин чтения"
    return f"≈ {round(minutes / 60)} ч чтения"


@register.filter
def book_age(year):
    """Сколько лет назад издана книга, со склонением слова «год»."""
    try:
        years = datetime.date.today().year - int(year)
    except (TypeError, ValueError):
        return ""
    return f"{years} {ru_plural(years, 'год,года,лет')} назад"


# ---------- Теги ----------

@register.simple_tag
def total_books():
    return Book.objects.count()


@register.simple_tag
def avg_price():
    return Book.objects.aggregate(avg=Avg("price"))["avg"] or 0


@register.simple_tag
def current_year():
    return datetime.date.today().year


@register.inclusion_tag("includes/genre_menu.html")
def genre_menu(active_slug=None):
    genres = Genre.objects.annotate(book_count=Count("books"))
    return {"genres": genres, "active_slug": active_slug}
