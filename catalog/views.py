from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib import messages
from .models import Book, UserStatus


def home(request):
    """Главная страница со списком пользователей"""
    # Аннотируем пользователей с подсчетом книг по статусам
    users = User.objects.annotate(
        book_count=Count('book_statuses'),
        reading_count=Count('book_statuses', filter=Q(book_statuses__reading_status='reading')),
        finished_count=Count('book_statuses', filter=Q(book_statuses__reading_status='finished'))
    )

    # Простая статистика
    total_books = Book.objects.count()
    total_users = users.count()

    # Общая статистика по статусам
    reading_now = UserStatus.objects.filter(reading_status='reading').count()
    finished_books = UserStatus.objects.filter(reading_status='finished').count()

    context = {
        'users': users,
        'total_books': total_books,
        'total_users': total_users,
        'reading_now': reading_now,
        'finished_books': finished_books,
    }
    return render(request, 'main_page.html', context)


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        if not username or not password:
            messages.error(request, 'Заполните все поля')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')

        # Создаем пользователя
        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        messages.success(request, f'Добро пожаловать, {username}!')
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'login.html')


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')


def book_list(request):
    """Список всех книг (все пользователи видят все книги)"""
    books = Book.objects.all()
    return render(request, 'catalog.html', {'books': books})


def book_detail(request):
    """Детальная информация о книге"""
    # Получаем ID книги из GET-параметра (так работает ваш шаблон)
    book_id = request.GET.get('id')

    if not book_id:
        messages.error(request, 'Книга не найдена')
        return redirect('catalog')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'Книга не найдена')
        return redirect('catalog')

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Обновление статуса
            reading_status = request.POST.get('reading_status')
            if reading_status:
                status, created = UserStatus.objects.update_or_create(
                    user=request.user,
                    book=book,
                    defaults={'reading_status': reading_status}
                )
                messages.success(request, 'Статус обновлен!')
                return redirect(f'/catalog/book/?id={book_id}')

            # Удаление книги
            if 'delete_book' in request.POST:
                book.delete()
                messages.success(request, 'Книга удалена!')
                return redirect('catalog')

    user_status = None
    if request.user.is_authenticated:
        try:
            user_status = UserStatus.objects.get(user=request.user, book=book)
        except UserStatus.DoesNotExist:
            pass

    context = {
        'book': book,
        'user_status': user_status,
    }
    return render(request, 'book.html', context)


@login_required
def book_create(request):
    """Создание новой книги"""
    if request.method == 'POST':
        # Простая обработка формы (как в вашем коде)
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        genre = request.POST.get('genre')
        description = request.POST.get('description')

        if title:  # Минимальная валидация
            book = Book.objects.create(
                title=title,
                author=author or 'Неизвестный автор',
                publication_year=publication_year,
                genre=genre or 'fiction',
                description=description
            )

            # Загрузка изображения если есть
            if 'cover_image' in request.FILES:
                book.cover_image = request.FILES['cover_image']
                book.save()

            # Создаем статус для пользователя
            UserStatus.objects.create(
                user=request.user,
                book=book,
                reading_status='not_started'
            )

            messages.success(request, 'Книга добавлена!')
            return redirect(f'/catalog/book/?id={book.id}')
        else:
            messages.error(request, 'Название книги обязательно!')

    return render(request, 'forms.html', {'action': 'create'})


@login_required
def book_edit(request):
    """Редактирование книги"""
    book_id = request.GET.get('id')

    if not book_id:
        return redirect('catalog')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'Книга не найдена')
        return redirect('catalog')

    if request.method == 'POST':
        # Обновляем данные книги
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = request.POST.get('publication_year', book.publication_year)
        book.genre = request.POST.get('genre', book.genre)
        book.description = request.POST.get('description', book.description)

        # Обновляем изображение если загружено
        if 'cover_image' in request.FILES:
            book.cover_image = request.FILES['cover_image']

        # Если отмечено "удалить обложку"
        if 'remove_cover' in request.POST and book.cover_image:
            book.cover_image.delete()

        book.save()
        messages.success(request, 'Книга обновлена!')
        return redirect(f'/catalog/book/?id={book_id}')

    context = {'book': book, 'action': 'edit'}
    return render(request, 'forms.html', context)


@login_required
def my_books(request):
    """Страница с книгами пользователя"""
    user_statuses = UserStatus.objects.filter(user=request.user)

    # Группируем по статусам
    status_groups = {
        'not_started': user_statuses.filter(reading_status='not_started'),
        'reading': user_statuses.filter(reading_status='reading'),
        'finished': user_statuses.filter(reading_status='finished'),
        'planned': user_statuses.filter(reading_status='planned'),
        'abandoned': user_statuses.filter(reading_status='abandoned'),
    }

    context = {
        'user_statuses': user_statuses,
        'status_groups': status_groups,
    }
    return render(request, 'profil.html', context)