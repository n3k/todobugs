from django.urls import path

import myapp.views as views

urlpatterns = [
    path('', views.index, name='index'),    

    path('account/register/'  , views.register  , name="register"),
    path('account/login/', views.do_login, name="login"),
    path('home', views.home, name="home"),
    path('account/settings', views.settings, name="settings"),
    path('account/profile', views.profile, name="profile"),
    path('account/logout', views.logout, name="logout"),
    path('account/passwdchg', views.passwdchg, name="passwdchg"),

    # /myapp/todo
    path('todo/add', views.create_todo, name="create_todo"),
    path('todo/<int:todo_id>', views.edit_todo, name="edit_todo"),
    path('todo/<int:todo_id>/tasks', views.tasks_handler, name="tasks_handler"),

    path('tasks/<int:task_id>', views.task_details, name="task_details"),
    

    # Cache this on reverse proxy 
    #path('todos/<int:year>/', views.todos_by_year),

    # /myapp/@user
    path('public/@<str:username>', views.public_profile, name='public_profile'),    
]