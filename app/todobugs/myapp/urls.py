from django.urls import path

import myapp.views as views

urlpatterns = [
    path('', views.index, name='index'),    

    path('account/register/'  , views.register  , name="register"),
    path('account/user_login/', views.user_login, name="user_login"),
    path('account/home/', views.home, name="home"),
    path('account/logout', views.logout, name="logout"),
]