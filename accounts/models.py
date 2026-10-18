from django.db import models
from django.contrib.auth.models import( AbstractBaseUser, BaseUserManager, PermissionsMixin )
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, phone_number, password = None, **extra_fields):
        if not phone_number:
            raise ValueError("phone number is required")
        phone_number = phone_number.strip() #удаляет пробелы в начале и в конце номера телефона
        user = self.model(phone_number = phone_number, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_supeuser(self, phone_number, password = None, **extra_fields):
        extra_fields.setdefault("is_staff" , True)
        extra_fields.setdefault("is_superuser" , True)
        extra_fields.setdefault("is_active" , True)
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_staff=True an is_superuser = True")
        return self.create_user(phone_number, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = AccountManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.phone_number