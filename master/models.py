from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Master(models.Model):
    GENDER_CHOISES = (
        ('MALE', 'Male'),
        ('FEMALE', "Female")

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usta_profile')
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOISES)
    address = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0, help_text="Ish tajribasi yillarda")
    bio = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.job.title})"


class Review(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1,6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.master.full_name} uchun sharh"


class Message(models.Model):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="sent_message")
    receiver = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="received_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

    class Meta:
        ordering = ["created_at"]