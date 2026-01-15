from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    """
    Класс, представляющий книгу в каталоге.
    """

    # Список жанров для выбора в форме
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

    # Название книги
    title = models.CharField(
        max_length=200,
        verbose_name='Название книги'
    )

    # Автор книги
    author = models.CharField(
        max_length=100,
        verbose_name='Автор',
        blank=True,  # Можно не указывать
        default='Неизвестный автор'  # Значение по умолчанию
    )

    # Год издания книги
    publication_year = models.IntegerField(
        verbose_name='Год издания',
        null=True,  # Может быть пустым в БД
        blank=True,  # Можно не указывать
        validators=[  # Проверка, что год между 1000 и 2100
            MinValueValidator(1000),
            MaxValueValidator(2100)
        ]
    )

    # Жанр книги
    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,  # Можно выбрать только из списка
        default='fiction',  # Значение по умолчанию - художественная литература
        verbose_name='Жанр'
    )

    # Краткое описание книги
    description = models.TextField(
        verbose_name='Краткое описание',
        blank=True  # Можно не указывать
    )

    # Картинка обложки книги
    cover_image = models.ImageField(
        upload_to='book_covers/',  # Картинки сохраняются в папку book_covers
        verbose_name='Обложка',
        blank=True,  # Можно не загружать
        null=True  # Может быть пустым в БД
    )

    def __str__(self):
        """
        Возвращает строковое представление книги.
        """
        return f'{self.title} ({self.author})'


class UserStatus(models.Model):
    """
    Класс для хранения статуса чтения книги у пользователя.
    """

    # Список статусов чтения для выбора в форме
    READING_STATUS = [
        ('not_started', 'Не начата'),
        ('reading', 'Читаю'),
        ('finished', 'Прочитана'),
        ('abandoned', 'Брошена'),
        ('planned', 'В планах'),
    ]

    # Ссылка на пользователя
    user = models.ForeignKey(
        User,  # Стандартная модель пользователя из Django
        on_delete=models.CASCADE,  # Если удалить пользователя, удалятся и его статусы
        related_name='book_statuses'  # Позволяет получить все статусы книг этого пользователя
    )

    # Ссылка на книгу
    book = models.ForeignKey(
        Book,  # Модель книги
        on_delete=models.CASCADE,  # Если удалить книгу, удалятся и статусы по ней
        related_name='user_statuses'  # Позволяет получить всех пользователей, читающих эту книгу, и их статусы
    )

    # Статус чтения
    reading_status = models.CharField(
        max_length=20,
        choices=READING_STATUS,  # Можно выбрать только из списка
        default='not_started',  # Значение по умолчанию - не начата
        verbose_name='Статус чтения'
    )

    def __str__(self):
        """
        Возвращает строковое представление информации о статусе чтения.
        """
        return f'{self.user.username} - {self.book.title}: {self.reading_status}'
