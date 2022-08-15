from django import forms 
from django.contrib.auth.models import User 
from myapp.models import UserProfile, Todo, Task

class UserForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email    = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    
    nickname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    website  = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio      = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    #picture  = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProfile
        fields = ('nickname', 'bio', 'website') #, 'picture')



# class UpdateUserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
    
#     class Meta:
#         model = User
#         fields = ('email', 'password')


# class UpdateUserProfileForm(forms.ModelForm):

#     class Meta:
#         model = UserProfile
#         fields = ('nickname', 'website', 'picture')



    
class TodoForm(forms.ModelForm):     
    name        = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    #public      = forms.(widget=forms.BooleanField(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Todo
        fields = ('name', 'description', 'public')


class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ('description',)