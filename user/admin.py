from django.contrib import admin

from .models import User, Commentary, Chat
# Register your models here.
admin.site.register(User)
admin.site.register(Commentary)
admin.site.register(Chat)