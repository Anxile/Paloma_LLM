from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import UserCollection, User
from .form import CreateNewUser

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.

def index(request):
    members = UserCollection.objects.all()
    if request.method == 'POST':
        if request.POST.get('delete'):
            uc = UserCollection.objects.get(id=request.POST.get('delete'))
            uc.delete()  
            return HttpResponse('User deleted')
        elif request.POST.get('edit'):
            uc.name = request.POST.get('edit_create')
            uc.save()
            return HttpResponse('User updated')
        elif request.POST.get('create'):
            uc = UserCollection(name=request.POST.get('edit_create'))
            uc.save()
    return render(request, 'index.html', {'members': members})

def create_user(request):
    if request.method == 'POST':
        f = CreateNewUser(request.POST)
        if f.is_valid():
            f_clean = f.cleaned_data
            name = f_clean['name']
            age = f_clean['age']
            usercollection = UserCollection(name=name, preprocessed=False)
            usercollection.save()
            u = User(name=name, age=age, usercollection=usercollection)
            u.save()
            return HttpResponse('User created')
        else:
            return HttpResponse('Form is not valid')
    else:
        f = CreateNewUser()
    return render(request, 'create.html', {'form': f})

def user_match(request, userid):
    item = UserCollection.objects.all()

    user = UserCollection.objects.get(id=userid)


    return render(request, 'todo_test.html', {'user': user})