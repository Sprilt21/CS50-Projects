from django.contrib import admin
from .models import User, Job, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Job)
admin.site.register(Message)