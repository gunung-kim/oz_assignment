from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin

class TodoListView(LoginRequiredMixin,ListView):
    queryset = Todo.objects.all().order_by('-end_date')
    template_name = 'todo_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        # print(f"{queryset}######")
        return queryset

class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    template_name='todo_detail.html'
    fields=('title','description','start_date','end_date','is_completed')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields=('title','description','start_date','end_date','is_completed')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class TodoUpdateView(LoginRequiredMixin,UpdateView):
    model = Todo
    template_name='todo_update.html'
    fields=('title','description','end_date','is_completed')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

class TodoDeleteView(LoginRequiredMixin,DeleteView):
    model = Todo

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == "GET":
            raise Http404
        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('todo:list')