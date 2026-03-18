from django.urls import path, include
from . import views

urlpatterns = [
    path('sign_up/',views.signup,name='sign_up'),
    path('accounts/login/',views.login,name='login'),
    path('todos/',include('todo.urls'))
]