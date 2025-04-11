from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import book_list

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Авторизация и регистрация
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Профиль пользователя
    path('profile/', views.profile, name='profile'),

    # Список книг
    path('books/', book_list, name='book_list'),

    # Книги по категориям
    path('category/<str:category_code>/', views.books_by_category, name='books_by_category'),

    # Тесты
    path('tests/', views.test_categories, name='test_categories'),
    path('tests/<slug:category_slug>/', views.category_tests, name='category_tests'),

    # Пройти тест
    path('test/<int:test_id>/', views.take_test, name='take_test'),

    # Результаты теста
    path('test/result/<int:test_id>/', views.test_result, name='test_result'),
    path('read/<int:book_id>/', views.read_pdf, name='read_pdf'),

]
