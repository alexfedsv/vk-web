from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_num>/', views.index, name='index'),
    path('hot/<int:page_num>/', views.hot, name='hot'),
    path('question/<int:question_id>/<int:page_num>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('tag/<target_tag>/<int:page_num>/', views.tag, name='tag'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('settings/', views.settings, name='settings'),
]
