from django.shortcuts import render, redirect

# Create your views here.

from myapp.forms import UserForm, UserProfileForm

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
#from django.core.url import reverse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

#####################






def register(request):

    # if request is POST
    if request.method == 'POST':

        #grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() # save to database
            user.set_password(user.password)
            user.save()


            #until we are ready to avoid integrity problems we set commit=False
            profile = profile_form.save(commit=False)

            #set user instance for profile
            profile.user = user

            # If profile picture was provided we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

                profile.save()   #saving the UserProfile model instance

            return redirect("user_login") # return user to login page


    else:
        # Not a HTTP POST,so we render the same empty  form
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registration.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        })


    
def user_login(request):
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
    return render(request, 'home.html')



def logout(request):
    response = HttpResponseRedirect('home')
    response.delete_cookie('sessionid')
    return response