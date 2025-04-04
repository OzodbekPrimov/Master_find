from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'Oddiy foydalanuvchi'),
        ('MASTER', 'Usta'),
        ('ADMIN', 'Admin')
    )
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='USER')

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usta_profile')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    # rating = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1,6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.usta.full_name} uchun sharh"

