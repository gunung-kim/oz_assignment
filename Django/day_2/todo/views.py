from django.shortcuts import render, redirect
from .models import Todo
from django.conf import settings
from django.contrib.auth.decorators import login_required

def root(request):
    return render(request,'root.html')

# @login_required(login_url=settings.LOGIN_URL)
def todo_list(request):
    if not request.user.is_authenticated:
        context = {"msg":"로그인한 유저만 접근 가능합니다"}
        return render(request,'todo_list.html',context)
    todos = Todo.objects.all()
    context = {'todos': todos}
    return render(request,'todo_list.html',context)

# @login_required(login_url=settings.LOGIN_URL)
def todo_detail(request,pk):
    if not request.user.is_authenticated:
        context = {"msg":"로그인한 유저만 접근 가능합니다"}
        return render(request,'todo_list.html',context)
    target_todo = Todo.objects.get(pk=pk)
    if not target_todo:
        raise Http404
    context = {'target_todo': target_todo}
    return render(request,'todo_detail.html',context)