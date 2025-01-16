from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('create/', views.create_task, name='create_task'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('mark_as_not_done/<int:pk>/', views.mark_as_not_done, name='mark_as_not_done'),
    path('mark_as_done/<int:pk>/', views.mark_as_done, name='mark_as_done'),
    
]
