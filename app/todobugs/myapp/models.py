from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64)
    bio      = models.TextField(blank=True)
    website  = models.CharField(blank=True, max_length=256)
    # picture  = models.ImageField(upload_to='profile_images/',\
    #                              blank=True
    #                             )
    def __str__(self):
        return self.user.username



class Todo(models.Model):

    owner       = models.ForeignKey(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=512)
    description = models.TextField()
    date        = models.DateField()
    completed   = models.BooleanField()
    public      = models.BooleanField()

    def __str__(self):
        return self.name





class Task(models.Model):

    todo        = models.ForeignKey(Todo, on_delete=models.CASCADE)    
    description = models.TextField()   
    completed   = models.BooleanField()
