from django.db import models

# Create your models here.
class Template(models.Model):
    prompt = models.CharField(max_length=200)
    user_info = models.CharField(max_length=400)    