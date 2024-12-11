from .models import Task
from django.forms import ModelForm, TextInput, Textarea
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи'}),
            'task': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание задачи'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

