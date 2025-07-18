from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/home.html', {'tasks': tasks})

@login_required
def add_task(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('home')
    return render(request, 'tasks/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'tasks/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('home')
