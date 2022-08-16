
from django.shortcuts import render, redirect
from django.http import QueryDict
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.core.serializers import serialize


from myapp.models import UserProfile, User, Todo, Task

# Create your views here.

from myapp.forms import TaskForm, TodoForm, UserForm, UserProfileForm

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

import datetime
import json

#from django.core.url import reverse


def index(request):
    welcome = "Welcome To The Club, Pal"
    welcome += "<br/>"
    welcome += "<a href='home'>home</a>"
    return HttpResponse(welcome)

#####################



def __check_email_is_unique(email):
    if User.objects.filter(email=email):    
        return False
    return True
    


def register(request):

    # if request is POST
    if request.method == 'POST':

        #grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            provided_email = user_form.cleaned_data['email']
            if __check_email_is_unique(provided_email) == False:
                return HttpResponse(f"The email {provided_email} is already registered!")

            user = user_form.save() # save to database
            user.set_password(user.password)
            user.save()


            #until we are ready to avoid integrity problems we set commit=False
            profile = profile_form.save(commit=False)

            #set user instance for profile
            profile.user = user

            # If profile picture was provided we need to get it from the input form and put it in the UserProfile model.
            #if 'picture' in request.FILES:
                #profile.picture = request.FILES['picture']

            profile.save()   #saving the UserProfile model instance

            return redirect("login") # return user to login page


    else:
        # Not a HTTP POST,so we render the same empty  form
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registration.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        })


    
def do_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #attempt to see if the username/password
        # combination is valid -
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # Login if user is active and valid 
                # Redirecting user back to home page 
                login(request, user)
                return redirect('home')
            else:
                # An inactive account indication !!!
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})



    
def home(request):
    #rendering our home page
    if request.user.is_authenticated:
        todos = Todo.objects.filter(owner=request.user)
        context = { 
            "todos": todos
        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')




def logout(request):
    response = HttpResponseRedirect('/myapp/home')
    response.delete_cookie('sessionid')
    return response



@csrf_exempt
@login_required(login_url="login")
def passwdchg(request):
    
    if request.method == 'GET':  
        user = request.user
  
        context= {
                'user'   : user,                
            }

        return render(request, 'passwdchg.html',  context)

    elif request.method == 'POST':        

        password = request.POST.get('password', '')
        if len(password) == 0:
            return HttpResponseBadRequest("No password submitted!")

        user = request.user
        user.set_password(password)
        user.save()

        return HttpResponse("Password changed successfully!")




@login_required(login_url="login")
@xframe_options_exempt
def settings(request):  
    if request.method == 'GET':  
        user = request.user
  
        context= {
                'user'   : user,
                'profile': user.userprofile,
            }

        return render(request, 'settings.html',  context)

    elif request.method == "PUT":
        put = QueryDict(request.body)

        nickname = put.get("nickname", "")
        email    = put.get("email", "")
        website  = put.get("website", "")
        bio_text = put.get("bio_text", "")

        try:
            validate_email(email)
        except ValidationError as e:
            return HttpResponseBadRequest("bad email, details: {}".format(e))
        
        if email != "":
            user = request.user
            user.email = email
            user.save()
        
        profile = user.userprofile

        if nickname != "":
            profile.nickname = nickname
        if website != "":
            profile.website  = website
        if bio_text != "":
            profile.bio = bio_text
        
        profile.save()

        return HttpResponse("settings successfully updated")

    elif request.method == "DELETE":
        return HttpResponse("DELETE THE ACCOUNT")
    else:
        HttpResponseNotAllowed("Not allowed")

@login_required(login_url="login")
def profile(request):
    response = HttpResponseRedirect(f'/myapp/public/@{request.user}')    
    return response


@login_required(login_url="login")
def create_todo(request):
    
    if request.method == "POST":
        todo_form = TodoForm(data=request.POST)
        if todo_form.is_valid():
            todo           = todo_form.save(commit=False) 
            todo.owner     = request.user            
            todo.completed = False
            todo.date      = datetime.date.today()
            todo.save()
            return redirect('home')
        else:
            return HttpResponseBadRequest("invalid todo form")

    else:
        todo_form = TodoForm()        

        return render(request, 'create_todo.html',
            {
                'todo_form': todo_form            
            })


@login_required(login_url="login")
def edit_todo(request, todo_id):
    
    if request.method == "PUT":
        todo = Todo.objects.filter(owner=request.user, id=todo_id).first()

        if not todo:
            return HttpResponseBadRequest("invalid todo id")

        put = QueryDict(request.body)

        todo_name = put.get("name", "")
        todo_desc = put.get("description_text", "")
        public    = put.get("public", "")
        
        todo.name        = todo_name
        todo.description = todo_desc
        if public != "":
            todo.public = True
        else:
            todo.public = False

        todo.save()

        return HttpResponse("User {} todo {} updated successfully".format(todo.owner, todo.id))

    elif request.method == "DELETE":
        Todo.objects.filter(owner=request.user, id=todo_id).delete()
        return HttpResponse("successfully deleted ToDo list with id: {}".format(todo_id))
        

    else:
        todo = Todo.objects.filter(owner=request.user, id=todo_id).first()

        return render(request, 'edit_todo.html',
            {
                'todo': todo
            })



@login_required(login_url="login")
def tasks_handler(request, todo_id):
    todo  = Todo.objects.filter(owner=request.user, id=todo_id).first()

    if request.method == "GET":        
        tasks = Task.objects.filter(todo=todo)      
        data = json.dumps([{'description': t.description, 'completed': t.completed} for t in tasks] )
        return HttpResponse(data, content_type="application/json")
        
    elif request.method == "POST":        
        
        try:
            data = request.body
            data_dict = json.loads(data.decode("utf-8")) 
            
            # Delete all and re-create
            Task.objects.filter(todo=todo).delete()        

            for t in data_dict:
                task_form = TaskForm()
                task = task_form.save(commit=False)
                task.description = t["description"]
                task.completed   = t["completed"]
                task.todo        = todo
                task.save()

        except Exception as e:
            return HttpResponseBadRequest("error during task update: {}".format(e))
        
        return HttpResponse({}, content_type="application/json")


    else:
        return HttpResponseNotAllowed("method not allowed")


@login_required(login_url="login")
def task_details(request, task_id):
    try:
        task = Task.objects.get(id=task_id)    
        data = json.dumps({'description': task.description, 'completed': task.completed})
        return HttpResponse(data, content_type="application/json")
    except:    
        return HttpResponse({}, content_type="application/json")


def public_profile(request, username):
    try:
        user  = User.objects.raw('SELECT id, username FROM auth_user WHERE username="{}" limit 1'.format(username))[0]    
        #print(user)
        todos = Todo.objects.filter(owner=user, public=True)
        public_todos = []

        for todo in todos:
            public_todo = {}
            tasks = Task.objects.filter(todo=todo)
            public_todo["todo_name"] = todo.name
            public_todo["todo_desc"] = todo.description
            p_tasks = []        
            for task in tasks:
                p_tasks.append({
                    "task_desc": task.description,
                    "task_completed": task.completed
                })
            public_todo["tasks"] = p_tasks
            public_todos.append(public_todo)


        context = {
            'user'   : user,
            'profile': user.userprofile,
            'public_todos'  : public_todos
        }
        
        return render(request, 'public_profile.html', context)
    except IndexError:
        return redirect('home')
