from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

Client, Courier, Admin = "Client", "Courier", "Admin"


class Manager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES_CHOICHES = (
        (Courier, Courier), 
        (Client, Client),
        (Admin, Admin)
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(choices=ROLES_CHOICHES, default=Client)
    is_staff = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
