from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import UserBase, User
from .form import CreateNewUser
from .data_seed import UserData

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.

def index(request):
    members = UserBase.objects.all()
    if request.method == 'POST':
        if request.POST.get('delete'):
            ub = UserBase.objects.get(id=request.POST.get('delete'))
            ub.delete()  
            return HttpResponse('User deleted')
        elif request.POST.get('edit'):
            ub.name = request.POST.get('edit_create')
            ub.save()
            return HttpResponse('User updated')
        elif request.POST.get('create'):
            ub = UserBase(name=request.POST.get('edit_create'))
            ub.save()
    return render(request, 'index.html', {'members': members})

def create_user(request):
    if request.method == 'POST':
        f = CreateNewUser(request.POST)
        if f.is_valid():
            f_clean = f.cleaned_data
            name = f_clean['name']
            age = f_clean['age']
            userbase = UserBase(name=name, preprocessed=False)
            userbase.save()
            u = User(name=name, age=age, userBase=userbase)
            u.save()
            return HttpResponse('User created')
        else:
            return HttpResponse('Form is not valid')
    else:
        f = CreateNewUser()
    return render(request, 'create.html', {'form': f})

def user_match(request, userid):
    item = UserBase.objects.all()

    user = UserBase.objects.get(id=userid)


    return render(request, 'todo_test.html', {'user': user})

def import_user(request):
    user_data = UserData.data

    count = 0
    
    for item in user_data:
        # 假设 UserBase 的 name 字段按照 "User_<User ID>" 的格式存储
        user_base_name = f"User_{item.get('User ID')}"
        
        try:
            # 若不存在，则创建对应的 UserBase 记录
            try:
                user_base = UserBase.objects.get(name=user_base_name)
            except UserBase.DoesNotExist:
                user_base = UserBase.objects.create(name=user_base_name, preprocessed=False)
            
            User.objects.create(
                userbase=user_base,  # 建立关联
                age=item.get('Age'),
                gender=item.get('Gender'),
                height=item.get('Height'),
                interests=item.get('Interests'),
                looking_for=item.get('Looking For'),
                children=item.get('Children') == 'Yes',
                education_level=item.get('Education Level'),
                occupation=item.get('Occupation'),
                swiping_history=item.get('Swiping History'),
                frequency_of_use=item.get('Frequency of Usage')
            )
            print(f"Created User for {user_base_name}")
            count += 1
            
        except Exception as e:
            print(f"Error creating User for {user_base_name}: {str(e)}")
    
    return HttpResponse(f"Created {count} users out of {len(user_data)}")