from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

user_role=[
    ("buyer","buyer"),
    ("farmer","farmer"),
    ("consultant","consultant")
]

class CustomUser(AbstractUser):
    role=models.CharField(max_length=10,choices=user_role,default="buyer")
    phone=models.CharField(max_length=15,blank=True,null=True)


    def __str__(self):
        return self.first_name + " " + self.last_name
    

