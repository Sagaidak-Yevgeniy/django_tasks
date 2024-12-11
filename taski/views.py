from django.shortcuts import render, redirect, get_object_or_404
from taski.models import Task
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages





def index(request):
   search_query = request.GET.get('search', '')
   if search_query:
        tasks = Task.objects.filter(title__icontains=search_query) | Task.objects.filter(task__icontains=search_query)
   else:
        tasks = Task.objects.all()
   return render(request, 'tasks/index.html', {'tasks': tasks})


# 🟢 Добавление записи
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'tasks/create/create_task.html', {'form': form})

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
    return render(request, 'tasks/edit/edit_task.html', {'form': form, 'task': task})

# 🟢 Удаление записи
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'tasks/delete/delete_task.html', {'task': task})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Имя пользователя уже занято.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email уже зарегистрирован.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти в систему.')
        return redirect('login')

    return render(request, 'tasks/register/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            
            # Проверяем, является ли пользователь администратором
            if user.is_superuser:  # Если это суперпользователь
                return redirect('home')
            
            # Проверяем, принадлежит ли пользователь группе "Администраторы"
            elif user.groups.filter(name='Администраторы').exists():  # Если он в группе "Администраторы"
                return redirect('home')
            
            # Если это обычный пользователь
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    return render(request, 'tasks/login/login.html')

def logout_view(request):
    logout(request)
    return redirect('dashboard')





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
