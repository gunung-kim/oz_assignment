"""
URL configuration for day_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import Http404
def root(request):
    return render(request,'root.html')

def gugu_list(request):
    numbers = range(1,10)
    return render(request,'gugu_list.html',{'numbers':numbers})

def gugu(request,num):
    if num ==0:
        raise Http404
    result=[]
    for i in range(1,10):
        result.append(num*i)
    context = {'result':result,'num':num}
    return render(request,'gugu.html',{'context':context})

movie_list=[
    {'title':'왕과 사는 남자','director':'정항준'},
    {'title':'백설공주','director':'마크 웹'},
    {'title':'하트맨','director':'정용기'},
    {'title':'프로젝트Y','director':'이환'},
]

def movies(request):
    return render(request,'movies.html',{'movie_list':movie_list})

def movie(request,num):
    target_movie = movie_list[num]
    title = target_movie['title']
    director = target_movie['director']
    return render(request,'movie.html',{'title':title,'director':director})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',root),
    path('gugu_list/',gugu_list),
    path('gugu_list/<int:num>/',gugu),
    path('movies/',movies),
    path('movies/<int:num>/',movie),
]
