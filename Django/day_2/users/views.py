from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as django_login

def signup(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)
    context = {'form': form}
    return render(request,'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request,data=request.POST)
    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL)
    context = {'form': form}
    return render(request,'registration/login.html', context)