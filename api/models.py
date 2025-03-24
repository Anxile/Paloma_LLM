from django.db import models

# Create your models here.


class UserBase(models.Model):
    name = models.CharField(max_length=200)
    preprocessed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True, null=True)
    verified = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name
    
class User(models.Model):
    userbase = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=200, null=True)
    height = models.IntegerField(null=True)
    interests = models.TextField(null=True)
    looking_for = models.CharField(max_length=200, null=True)
    children = models.BooleanField(default=False, null=True)
    education_level = models.CharField(max_length=200, null=True)
    occupation = models.CharField(max_length=200, null=True)
    swiping_history = models.IntegerField(null=True)
    frequency_of_use = models.CharField(max_length=200, null=True)

    # def __str__(self):
    #     user = UserCollection.objects.get(name=User.objects.get(name=self.name).usercollection)
    #     return self.name+' Processed: '+str(user.preprocessed)
    def __str__(self):
        return self.userbase.name
    
class UserFeature(models.Model):
    userbase = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    feature_vector = models.JSONField()
    context = models.CharField(max_length=200)  #dating, friendship, business, etc