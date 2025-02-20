from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextChoices, \
    ImageField, DateField

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class Employee(AbstractUser):
    class GenderChoices(TextChoices):
        MALE = "male", "MALE"
        FEMALE = "female", 'FEMELE'

    class RoleChoices(TextChoices):
        DRIVER = "driver", "Driver"
        ADMIN = "admin", "Admin"

    phone_number = CharField(max_length=20, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    username = None
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    birth_date = DateField(null=True,blank=True)
    gender = CharField(max_length=10, choices=GenderChoices.choices)
    passport = ImageField(upload_to='media/driver/passports/')
    prava = ImageField(upload_to='media/driver/prava/')
    role = CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.DRIVER)
