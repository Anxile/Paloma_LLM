from django.db import models

class UserBase(models.Model):
    name = models.CharField(max_length=200)
    preprocessed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True, null=True)
    verified = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name