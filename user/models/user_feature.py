from django.db import models
from .user_base import UserBase

class UserFeature(models.Model):
    userbase = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    feature_vector = models.JSONField()
    context = models.CharField(max_length=200)  #dating, friendship, business, etc