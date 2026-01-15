from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib import messages
from .models import Book, UserStatus
from .forms import BookForm, StatusForm


def main_page(request):
    """Главная страница со статистикой"""
    users = User.objects.annotate(
        book_count=Count('book_statuses', distinct=True),
        reading_count=Count('book_statuses',
                            filter=Q(book_statuses__reading_status='reading')),
        finished_count=Count('book_statuses',
                             filter=Q(book_statuses__reading_status='finished'))
    ).order_by('-book_count')

    context = {
        'users': users,
        'total_books': Book.objects.count(),
        'total_users': User.objects.count(),
        'reading_now': UserStatus.objects.filter(reading_status='reading').count(),
        'finished_total': UserStatus.objects.filter(reading_status='finished').count(),
    }
    return render(request, 'main_page.html', context)


@login_required
def book_list(request):
    """Список всех книг"""
    books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books})


@login_required
def book_create(request):
    """Добавление новой книги"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            # Создаем связь с пользователем
            UserStatus.objects.create(
                user=request.user,
                book=book,
                reading_status='not_started'
            )
            messages.success(request, 'Книга успешно добавлена!')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    """Редактирование книги"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно обновлена!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/book_form.html', {'form': form})


@login_required
def book_delete(request, pk):
    """Удаление книги"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книга удалена!')
        return redirect('book_list')
    return render(request, 'catalog/book_confirm_delete.html', {'book': book})


@login_required
def update_status(request, pk):
    """Изменение статуса чтения книги"""
    book = get_object_or_404(Book, pk=pk)
    user_status, created = UserStatus.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'reading_status': 'not_started'}
    )

    if request.method == 'POST':
        form = StatusForm(request.POST, instance=user_status)
        if form.is_valid():
            form.save()
            messages.success(request, f'Статус обновлен на: {user_status.get_reading_status_display()}')
            return redirect('book_list')
    else:
        form = StatusForm(instance=user_status)

    return render(request, 'catalog/update_status.html', {
        'form': form,
        'book': book
    })
