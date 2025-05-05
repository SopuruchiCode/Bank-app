from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from random import choices
from string import digits

def generate_bvn():
    mydigits = digits
    return ''.join(choices(mydigits,k=8))

class CustomUserManager(BaseUserManager):
    def create_user(self, bvn, password=None, **extra_fields):
        if not bvn:
            raise ValueError("Bvn must be set")
        user = self.model(bvn = bvn, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, bvn, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff = True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser = True')

        user =  self.create_user(bvn, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    username = None
    bvn = models.CharField(
                            unique=True,
                            default=generate_bvn,
                            max_length=8,
                            editable=False,
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    USERNAME_FIELD = "bvn"
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = CustomUserManager()
    def __str__(self):
        return f"{self.bvn}"