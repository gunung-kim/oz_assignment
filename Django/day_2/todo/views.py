from django.shortcuts import render
from .models import Todo

def root(request):
    return render(request,'root.html')

def todo_list(request):
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request,'todo_list.html',context)

def todo_detail(request,todo_id):
    target_todo = Todo.objects.get(id=todo_id)
    context = {'target_todo': target_todo}
    return render(request,'todo_detail.html',context)