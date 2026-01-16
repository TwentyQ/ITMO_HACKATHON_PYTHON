from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.book_list, name='catalog'),
    path('catalog', views.book_list, name='catalog_no_slash'),
    path('catalog/new/', views.book_create, name='book_create'),
    path('catalog/book/', views.book_detail, name='book_detail'),
    path('catalog/edit/', views.book_edit, name='book_edit'),
    path('profil/', views.my_books, name='profil'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]