from django.shortcuts import render, redirect, get_object_or_404,reverse
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import TodoCreate, TodoForm
from django.views.decorators.http import require_http_methods
from django.db.models import Q

def root(request):
    return render(request,'root.html')

@login_required()
def todo_list(request):
    user_todo = Todo.objects.filter(author=request.user).order_by('-create_at')
    if not user_todo:
        return render(request,'todo_list.html',{'todos':None,'msg':'아직 게시글이 없습니다'})
    q = request.GET.get('q')
    if q:
        user_todo = user_todo.filter(
            Q(title__icontains=q),
        )
    paginator = Paginator(user_todo,10)
    page = request.GET.get('page',1)
    page_obj = paginator.get_page(page)
    context = {'todos': user_todo,'page_obj':page_obj}
    return render(request,'todo_list.html',context)

@login_required()
def todo_detail(request,pk):
    target_todo = get_object_or_404(Todo,pk=pk,author=request.user)
    context = {'target_todo': target_todo.__dict__}
    return render(request,'todo_detail.html',context)

@login_required()
def todo_create(request):
    form = TodoCreate(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = request.user
        todo.save()
        return redirect(reverse('todo_detail',kwargs={'pk':todo.pk}))
    context = {'form': form}
    return render(request,'todo_create.html',context)

@login_required()
def todo_update(request,pk):
    todo = get_object_or_404(Todo,pk=pk,author=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
          form.save()
        return redirect(reverse('todo_detail',kwargs={"pk":pk}))
    else:
        form = TodoForm(instance=todo)
    context = {'form':form}
    return render(request,'todo_update.html',context)

@login_required()
@require_http_methods(['POST'])
def todo_delete(request,pk):
    todo = get_object_or_404(Todo,pk=pk,author=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))
