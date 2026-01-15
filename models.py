from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    READING_STATUS_CHOICES = [
        ('not_started', 'Не начата'),
        ('reading', 'Читаю'),
        ('finished', 'Прочитана'),
    ]
    
    GENRE_CHOICES = [
        ('fiction', 'Художественная литература'),
        ('non_fiction', 'Научная литература'),
        ('fantasy', 'Фэнтези'),
        ('sci_fi', 'Научная фантастика'),
        ('mystery', 'Детектив'),
        ('biography', 'Биография'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    publication_year = models.IntegerField(verbose_name="Год издания")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='fiction', verbose_name="Жанр")
    description = models.TextField(blank=True, verbose_name="Описание")
    reading_status = models.CharField(
        max_length=20, 
        choices=READING_STATUS_CHOICES, 
        default='not_started',
        verbose_name="Статус чтения"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.author})"
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']
