from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Художественная литература'),
        ('fantasy', 'Фэнтези'),
        ('scifi', 'Научная фантастика'),
        ('detective', 'Детектив'),
        ('romance', 'Роман'),
        ('biography', 'Биография'),
        ('history', 'История'),
        ('science', 'Наука'),
        ('self_help', 'Саморазвитие'),
        ('other', 'Другое'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Название книги'
    )
    author = models.CharField(
        max_length=100,
        verbose_name='Автор',
        blank = True,
        default = 'Неизвестный автор'
    )
    publication_year = models.IntegerField(
        verbose_name='Год издания',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2100)
        ]
    )
    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        default='fiction',
        verbose_name='Жанр'
    )
    description = models.TextField(
        verbose_name='Краткое описание',
        blank=True
    )
    cover_image = models.ImageField(
        upload_to='book_covers/',
        verbose_name='Обложка',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.title} ({self.author})'


class UserStatus(models.Model):
    READING_STATUS = [
        ('not_started', 'Не начата'),
        ('reading', 'Читаю'),
        ('finished', 'Прочитана'),
        ('abandoned', 'Брошена'),
        ('planned', 'В планах'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='book_statuses'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='user_statuses'
    )

    reading_status = models.CharField(
        max_length=20,
        choices=READING_STATUS,
        default='not_started',
        verbose_name='Статус чтения'
    )

    def __str__(self):
        return f'{self.user.username} - {self.book.title}: {self.reading_status}'