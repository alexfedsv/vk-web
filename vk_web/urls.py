"""
URL configuration for vk_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_num>/', views.index, name='index'),
    path('hot/<int:page_num>/', views.hot, name='hot'),
    path('question/<int:question_id>/<int:page_num>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('tag/<target_tag>/<int:page_num>/', views.tag, name='tag'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('settings/', views.settings, name='settings'),
    path('admin/', admin.site.urls),
]
