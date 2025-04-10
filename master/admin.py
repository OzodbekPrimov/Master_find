from django.contrib import admin
from .models import Review, Job, Master, Message
# Register your models here.

admin.site.site_header = "Master find admin panel"


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ('id',)
    search_fields = ('title',)


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name',  'phone_number', 'city', 'job', 'is_approved')
    search_fields = ('city', 'job__title')
    list_filter = ('city', 'job', 'is_approved')
    ordering = ('id',)


admin.site.register(Review)
admin.site.register(Message)
