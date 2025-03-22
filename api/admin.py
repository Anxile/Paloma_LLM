from django.contrib import admin
from .models import UserCollection, User

# Register your models here.
admin.site.register(UserCollection)
admin.site.register(User)
