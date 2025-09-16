from django.db import models
from django.contrib.auth.models import AbstractUser
import string,random
from django.utils import timezone

# Create your models here.

user_role=[
    ("buyer","buyer"),
    ("farmer","farmer"),
    ("consultant","consultant")
]

class CustomUser(AbstractUser):
    role=models.CharField(max_length=10,choices=user_role,default="buyer")
    phone=models.CharField(max_length=15,blank=True,null=True)
    email=models.EmailField(unique=True)
    otp=models.CharField(max_length=6,blank=True,null=True)
    otp_expiry=models.DateTimeField(blank=True,null=True)
    is_verified=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=["username"]

           
    def __str__(self):
        return self.first_name + " " + self.last_name
    

    def generate_otp(self):
        self.otp="".join(random.choices(string.digits,k=6))
        self.otp_expiry=timezone.now() + timezone.timedelta(minutes=10)
        self.save(update_fields=["otp","otp_expiry"])


    def verify_otp(self,otp):
        if self.otp ==otp  and self.otp_expiry >timezone.now():
            return True
        else:
            return False     
