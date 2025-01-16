from django.shortcuts import render, redirect
from taski.models import Task  # Импортируем модель Task из другого приложения
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages





def dashboard_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = Task.objects.filter(title__icontains=search_query) | Task.objects.filter(task__icontains=search_query)
    else:
        tasks = Task.objects.all()
    return render(request, 'dashboard/dashboard.html', {'tasks': tasks})




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

    return render(request, 'dashboard/register/register.html')


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

    return render(request, 'dashboard/login/login.html')



def logout_view(request):
    logout(request)
    return redirect('dashboard')



