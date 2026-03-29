from django.urls import path, include
from . import views

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('',include('django.contrib.auth.urls')),
    path('verify/',views.verify_email,name='verify_email'),
]