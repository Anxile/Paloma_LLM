from django import forms
from .models import User

class CreateNewUser(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    age = forms.IntegerField(label='Age')
    usercollection = forms.ModelChoiceField(queryset=User.objects.all())