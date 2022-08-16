from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from webadmin.models import User

from subprocess import Popen, PIPE


def index(request):
    return HttpResponse("<h1>Webadmin!</h1>")


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
                try:
                    user  = User.objects.raw('SELECT id, username FROM auth_user WHERE is_superuser = 1 AND username= %s', [user.username])[0]    
                    # Login if user is active and valid 
                    # Redirecting user back to home page 
                    login(request, user)
                    return redirect('webadmin_home')
                except IndexError:
                    return HttpResponseForbidden("This account does not have the required privileges")
                
            else:                
                return HttpResponseForbidden("This account is disabled")
        else:
            return HttpResponseForbidden("Invalid login details supplied.")
    else:
        return render(request, 'webadmin_login.html', {})


@login_required(login_url="webadmin_login")
def do_logout(request):
    logout(request)
    return redirect('webadmin_login')

@login_required(login_url="webadmin_login")
def home(request):
    if request.user.is_authenticated:  
        user = request.user
        try:
            user  = User.objects.raw('SELECT id, username FROM auth_user WHERE is_superuser = 1 AND username= %s', [user.username])[0]          
            return render(request, 'webadmin_home.html', { "user": request.user })
        except IndexError:
            return HttpResponseForbidden("This account does not have the required privileges")


@login_required(login_url="webadmin_login")        
def post_ping(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  
            user = request.user
            try:
                user  = User.objects.raw('SELECT id, username FROM auth_user WHERE is_superuser = 1 AND username= %s', [user.username])[0]                          

                target_host = request.POST.get('target_host')

                if ";" in target_host:
                    return HttpResponseBadRequest("bad boy")

                process = Popen(['ping -c 2 {}'.format(target_host)], shell=True, stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                
                return HttpResponse("r: {}".format(stdout.decode('utf-8')))


            except IndexError:
                return HttpResponseForbidden("This account does not have the required privileges")
