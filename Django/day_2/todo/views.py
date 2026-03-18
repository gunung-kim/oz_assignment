from django.shortcuts import render, redirect
from .models import Todo
from django.conf import settings

def root(request):
    return render(request,'root.html')

def todo_list(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request,'todo_list.html',context)

def todo_detail(request,pk):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    target_todo = Todo.objects.get(pk=pk)
    context = {'target_todo': target_todo}
    return render(request,'todo_detail.html',context)