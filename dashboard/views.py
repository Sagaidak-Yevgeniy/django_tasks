from django.shortcuts import render
from taski.models import Task  # Импортируем модель Task из другого приложения


def dashboard_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = Task.objects.filter(title__icontains=search_query) | Task.objects.filter(task__icontains=search_query)
    else:
        tasks = Task.objects.all()
    return render(request, 'dashboard.html', {'tasks': tasks})