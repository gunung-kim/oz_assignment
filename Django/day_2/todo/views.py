from django.shortcuts import render, redirect
from .models import Todo
from django.conf import settings
from django.contrib.auth.decorators import login_required

def root(request):
    return render(request,'root.html')

@login_required(login_url=settings.LOGIN_URL)
def todo_list(request):
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request,'todo_list.html',context)

@login_required(login_url=settings.LOGIN_URL)
def todo_detail(request,pk):
    target_todo = Todo.objects.get(pk=pk)
    if not target_todo:
        raise Http404
    context = {'target_todo': target_todo}
    return render(request,'todo_detail.html',context)