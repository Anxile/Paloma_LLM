from django.db import models

# Create your models here.


class UserCollection(models.Model):
    name = models.CharField(max_length=200)
    preprocessed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class User(models.Model):
    usercollection = models.ForeignKey(UserCollection, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    age = models.IntegerField()

    # def __str__(self):
    #     user = UserCollection.objects.get(name=User.objects.get(name=self.name).usercollection)
    #     return self.name+' Processed: '+str(user.preprocessed)
    def __str__(self):
        return self.name + ' Processed: ' + str(self.usercollection.preprocessed)