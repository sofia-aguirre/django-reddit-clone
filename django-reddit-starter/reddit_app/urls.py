from django.urls import path
from . import views

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[

    path('', views.index, name='index'),
    path('posts', posts_list),
    path('posts/new', posts_create),
    path('posts/<int:pk>', posts_detail),
    path('posts/<int:pk>/comments/new', comment_create),

    path('register', views.register, name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('logout', views.user_logout, name='logout'),

    path('api/users', views.sendJson, name='sendJson'),
    path('special',views.special, name='special'),
]