from django.urls import path
from forum import views


urlpatterns = [
    path('', views.home, name='index'),  
    path('topic/<int:id>/', views.topic_detail, name='topic_detail'), 
    path('topic/create/', views.create_topic, name='create_topic'), 
    path('login/', views.user_login, name='login'), 
    path('register/', views.register, name='register'), 
    path('logout/', views.user_logout, name='logout'),  
]
