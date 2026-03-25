from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm
from .models import Todo,Comment
from django.contrib.auth.mixins import LoginRequiredMixin

class TodoListView(LoginRequiredMixin,ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(author=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()
        queryset = queryset.order_by('-create_at')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset

class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    # queryset = Todo.objects.all().prefetch_related('comments','comments__user')
    template_name= 'todo/todo_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs['pk']).prefetch_related('comments','comments__user')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user:
            if not self.request.user.is_superuser:
                raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object.comments.all(),20)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context.update({
            "page_obj":page_obj,
            "comment_form":CommentForm(),
            "todo" : self.object.__dict__,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('todo_delist',kwargs={'pk':self.object.pk})

class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Todo
    template_name = 'todo/todo_create.html'
    fields=('title','description','start_date','end_date','is_completed')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo_detail',kwargs={'pk':self.object.pk})

class TodoUpdateView(LoginRequiredMixin,UpdateView):
    model = Todo
    template_name= 'todo/todo_update.html'
    fields=('title','description','end_date','is_completed')

    def get_object(self,queryset=None):
        self.object = super().get_object(queryset)
        if self.object != self.request.user:
            if not self.request.user.is_superuser:
                raise Http404
        return self.object

    def get_success_url(self):
        return reverse_lazy('todo_detail',kwargs={'pk':self.object.pk})

class TodoDeleteView(LoginRequiredMixin,DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object != self.request.user:
            if not self.request.user.is_superuser:
                raise Http404
        return self.object

    def get_success_url(self):
        return reverse_lazy('todo_list')

class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'todo_pk'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = Todo.objects.get(pk=self.kwargs['todo_pk'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo_detail',kwargs={'pk':self.object.todo.pk})

class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment/comment_update.html'

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs['pk'])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            if not self.request.user.is_superuser:
                raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo_detail',kwargs={'pk':self.object.todo.pk})

class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment

    def get_queryset(self):
        return super().get_queryset().filter(pk=self.kwargs['pk'])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user != self.object.user:
            if not self.request.user.is_superuser:
                raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def form_valid(self, form):
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo_detail',kwargs={'pk':self.object.todo.pk})


