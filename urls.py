from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('book/add/', views.add_book_view, name='add_book'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('book/<int:book_id>/edit/', views.edit_book_view, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book_view, name='delete_book'),
    path('book/<int:book_id>/update-status/', views.update_reading_status, name='update_status'),
]
