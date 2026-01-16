from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'user', 'reading_status', 'created_at')
    list_filter = ('reading_status', 'genre', 'created_at')
    search_fields = ('title', 'author', 'user__username')
    ordering = ('-created_at',)
  
