from django.shortcuts import render, redirect, get_object_or_404
from taski.models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def is_admin_user(user):

    if user.is_superuser or user.groups.filter(name='Администраторы').exists():
        return True
    raise PermissionDenied("Доступ запрещен")  # Возвращает ошибку 403

admin_required = user_passes_test(is_admin_user)


@admin_required
def index(request):
   
   search_query = request.GET.get('search', '')
   if search_query:
        tasks = Task.objects.filter(title__icontains=search_query) | Task.objects.filter(task__icontains=search_query)
   else:
        tasks = Task.objects.all()
   return render(request, 'tasks/index.html', {'tasks': tasks})



def custom_permission_denied_view(request, exception=None):
     return render(request, 'errors/403.html', status=403)

def custom_page_not_found_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)

# 🟢 Добавление записи
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'tasks/create/create_task.html', {'title_task': 'Создать задачу','form': form})

# 🟢 Редактирование записи
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit/edit_task.html', {'title_task': 'Редактировать задачу!!!!!!!!!!!!!!!', 'form': form, 'task': task})

# 🟢 Удаление записи
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'tasks/delete/delete_task.html', {'task': task})



def mark_as_not_done(request, pk):
    """Отметить задачу как невыполненную"""
    # Получаем задачу по её первичному ключу (pk)
    task = get_object_or_404(Task, pk=pk)
    # Меняем статус задачи на "не выполнена"
    task.status = False  
    # Сохраняем изменения в базе данных
    task.save()
    # Перенаправляем пользователя на домашнюю страницу
    return redirect('home') 

def mark_as_done(request, pk):
    """Отметить задачу как выполненную"""
    # Получаем задачу по её первичному ключу (pk)
    task = get_object_or_404(Task, pk=pk)
    # Устанавливаем статус задачи как "выполнена"
    task.status = True  
    # Сохраняем изменения в базе данных
    task.save()
    # Перенаправляем пользователя на домашнюю страницу
    return redirect('home') 
