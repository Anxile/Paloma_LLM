from django.contrib import admin
from .models import UserBase, User, UserFeature

# Register your models here.
admin.site.register(UserBase)
admin.site.register(User)
admin.site.register(UserFeature)
