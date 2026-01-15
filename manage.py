import os
import sys


def main():
    """Run administrative tasks."""

    # Устанавливаем настройки Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_catalog_project.settings')

    try:
        # Пытаемся импортировать execute_from_command_line из Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Если Django не установлен или не может быть импортирован
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Выполняем команду Django
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
