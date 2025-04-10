from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqami '+998#########' formatida bo'lishi kerak."
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email,  password=None,  **extra_fields):
        """Oddiy userlar uchun"""
        if not email:
            raise ValueError("Email kiritilishi shart")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # parolni xavfsiz saqlash uchun
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Admin yoki superuser yaratish """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "ADMIN")  # role avtomatik admin bo'ladi
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser uchun is_staff=True bo'lishi kerak.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser uchun is_superuser=True bo'lishi kerak.")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'Oddiy foydalanuvchi'),
        ('MASTER', 'Usta'),
        ("ADMIN", 'Admin')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[phone_regex])

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username}"
