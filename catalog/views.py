from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
from .models import Book
from catalog.forms import RegistrationForm, BookForm

def main_page(request):
    # Главная страница со списком пользователей и количеством книг
    users = User.objects.annotate(book_count=Count('books')).filter(book_count__gt=0)
    context = {
        'users': users,
    }
    return render(request, 'main_page.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('catalog')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalog')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('main_page')

@login_required
def catalog_view(request):
    # Показываем книги только текущего пользователя
    books = Book.objects.filter(user=request.user)
    context = {
        'books': books,
    }
    return render(request, 'catalog.html', context)

@login_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, 'Книга успешно добавлена!')
            return redirect('catalog')
    else:
        form = BookForm()
    return render(request, 'forms.html', {'form': form, 'title': 'Добавить книгу'})

@login_required
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно обновлена!')
            return redirect('catalog')
    else:
        form = BookForm(instance=book)
    return render(request, 'forms.html', {'form': form, 'title': 'Редактировать книгу'})

@login_required
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Пользователь может видеть только свои книги или все? 
    # Здесь показываем только если это книга текущего пользователя
    if book.user != request.user:
        messages.error(request, 'У вас нет доступа к этой книге')
        return redirect('catalog')
    return render(request, 'book.html', {'book': book})

@login_required
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Книга успешно удалена!')
        return redirect('catalog')
    return render(request, 'catalog.html', {'book': book})

@login_required
def update_reading_status(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('reading_status')
        if new_status in dict(Book.READING_STATUS_CHOICES):
            book.reading_status = new_status
            book.save()
            messages.success(request, 'Статус чтения обновлен!')
    return redirect('catalog')
  
