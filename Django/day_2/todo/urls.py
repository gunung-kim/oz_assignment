from django.urls import path
from . import views,cb_views

urlpatterns = [
    # FBV
    path('FBV/',views.todo_list),
    path('FBV/<int:pk>/',views.todo_detail),
    path('FBV/<int:pk>/update/',views.todo_update),
    path('FBV/create/',views.todo_create),
    path('FBV/<int:pk>/delete/',views.todo_delete),

    #CBV
    path('CBV/', cb_views.TodoListView.as_view(), name='todo_list'),
    path('CBV/<int:pk>/', cb_views.TodoDetailView.as_view(), name='todo_detail'),
    path('CBV/create/', cb_views.TodoCreateView.as_view(), name='todo_create'),
    path('CBV/<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='todo_update'),
    path('CBV/<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='todo_delete'),

    #comment
    path('comment/create/<int:todo_pk>/',cb_views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/',cb_views.CommentUpdateView.as_view(),name='comment_update'),
    path('comment/<int:pk>/delete/',cb_views.CommentDeleteView.as_view(),name='comment_delete'),
]