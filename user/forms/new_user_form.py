from django import forms
from ..models import User

class CreateNewUser(forms.Form):
    name = forms.CharField(label='name', max_length=200)
    age = forms.IntegerField(label='Age')
    gender = forms.CharField(label= 'gender', max_length=200)
    height = forms.IntegerField(label= 'height')
    interests = forms.CharField(label= 'interests')
    looking_for = forms.CharField(label= 'looking_for', max_length=200)
    children = forms.BooleanField(label='children')
    education_level = forms.CharField(label= 'education_level', max_length=200)
    occupation = forms.CharField(label= 'occupation', max_length=200)
    swiping_history = forms.IntegerField(label= 'swiping_history')
    frequency_of_use = forms.CharField(label= 'frequency_of_use', max_length=200)