from user.models import UserBase
from django.shortcuts import render
from django.http import HttpResponse
from user.models.user import User
from pre_process.services.embeddingService import embedding_extract
from ..forms import CreateNewUser

def create_user(request):
    if request.method == 'POST':
        f = CreateNewUser(request.POST)
        if f.is_valid():
            f_clean = f.cleaned_data
            name = f_clean['name']
            age = f_clean['age']
            gender = f_clean['gender']
            height = f_clean['height']
            interests = f_clean['interests']
            looking_for = f_clean['looking_for']
            children = f_clean['children']
            education_level = f_clean['education_level']
            occupation = f_clean['occupation']
            swiping_history = f_clean['swiping_history']
            frequency_of_use = f_clean['frequency_of_use']
            userbase = UserBase(name=name, preprocessed=False)
            userbase.save()
            u = User(age=age, userbase=userbase, gender = gender, height = height, interests = interests, looking_for = looking_for, children = children, education_level = education_level, occupation = occupation, swiping_history = swiping_history, frequency_of_use = frequency_of_use)
            u.save()
            embedding_extract(u)
            return HttpResponse('User created')
        else:
            return HttpResponse('Form is not valid')
    else:
        f = CreateNewUser()
    return render(request, 'create.html', {'form': f})