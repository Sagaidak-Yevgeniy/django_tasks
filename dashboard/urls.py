from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # Отображение всех задач в режиме "только чтение"
     path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
