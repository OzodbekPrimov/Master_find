from django.contrib import admin
from .models import Review, Job, Master, User
# Register your models here.

admin.site.register(Review)
admin.site.register(Job)
admin.site.register(Master)
admin.site.register(User)
