from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from random import randint
from django.contrib.auth.models import User


def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)

class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 ,null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.password = random_with_N_digits(12)
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    email=models.EmailField(max_length=255, unique=True)
    dob = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='media', blank=True, null=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    public_key = models.CharField(max_length=12,  unique=True, blank=True, null=True)
    private_key = models.CharField(max_length=255, unique=True, blank=True)
    pin_code=models.CharField(max_length=6,blank=True)

    def __str__(self):
        return self.public_key