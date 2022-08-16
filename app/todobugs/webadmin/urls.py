from django.urls import path

import webadmin.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.do_login, name="webadmin_login"),
    path('logout', views.do_logout, name="webadmin_logout"),
    path('home', views.home, name="webadmin_home"),
    path('ping', views.post_ping, name="webadmin_ping"),
]
