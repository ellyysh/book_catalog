# Лабораторная работа №1. Django: модели, шаблоны и теги

## Наследование шаблонов

* `base.html` объявляет `{% block title %}` и `{% block content %}`.
* `book_list.html` и `book_detail.html` делают `{% extends "base.html" %}` и переопределяют блоки;
  в `title` используется `{{ block.super }}`.
* `{% include %}` подключает шапку, подвал и карточку книги (с передачей переменных через `with`).

## Встроенные теги и фильтры

| Что | Где используется |
|---|---|
| `{% for %} … {% empty %}`, `forloop.counter` | список книг, меню жанров |
| `{% if %} / {% else %}` | наличие, активный жанр, страна автора |
| `{% url %}` | все ссылки |
| `{% cycle … as … silent %}` | чередование фона карточек |
| `{% with %}` | детальная страница (`author=book.author`) |
| `{% firstof %}` | заголовок списка |
| `{% now %}` | подвал |
| `{% load static %}` / `{% static %}` | подключение CSS |
| `length`, `upper`, `default`, `truncatewords` | список / карточка |
| `floatformat`, `yesno`, `date`, `linebreaks` | карточка / детальная |
| `intcomma` (django.contrib.humanize) | детальная страница |

## Кастомные фильтры и теги (`catalog/templatetags/book_extras.py`)

Подключение: `{% load book_extras %}`

**Фильтры**

| Фильтр | Пример | Результат |
|---|---|---|
| `rub` | `{{ 1250\|rub }}` | `1 250,00 ₽` |
| `stars` | `{{ 4.6\|stars }}` | `★★★★★` |
| `ru_plural` | `{{ 5\|ru_plural:"книга,книги,книг" }}` | `книг` |
| `reading_time` | `{{ 480\|reading_time }}` | `≈ 16 ч чтения` |
| `book_age` | `{{ 1967\|book_age }}` | `59 лет назад` |

**Теги**

| Тег | Тип | Что делает |
|---|---|---|
| `{% total_books %}` / `{% total_books as count %}` | simple_tag | число книг в базе (шапка) |
| `{% avg_price as avg %}` | simple_tag | средняя цена (страница списка) |
| `{% current_year %}` | simple_tag | текущий год (подвал) |
| `{% genre_menu active_slug %}` | inclusion_tag | меню жанров с количеством книг |
