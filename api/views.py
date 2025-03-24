from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import UserBase, User, UserFeature
from .form import CreateNewUser
from .data_seed import UserData
from sklearn.metrics.pairwise import cosine_similarity

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
            embedding(u)
            return HttpResponse('User created')
        else:
            return HttpResponse('Form is not valid')
    else:
        f = CreateNewUser()
    return render(request, 'create.html', {'form': f})

def user_match(request, userid):
    similarity = []
    user = UserBase.objects.get(id=userid)
    collection = UserBase.objects.all()
    if user.preprocessed == True:
        for match in collection:
            if match.preprocessed == False:
                embedding(User.objects.get(userbase=match))
            similarity.append(compute_similarity(user, match))
    else:
        embedding(User.objects.get(userbase=user))
    print(similarity)
    return render(request, 'todo_test.html', {'user': user, 'set': collection, 's' : similarity})


def embedding(new_user, model="text-embedding-3-small", context="dating"):
    # new_user 是 User 实例，通过外键获取关联的 UserBase 实例
    base = new_user.userbase
    # 获取对应的 UserFeature，注意确保记录存在，否则需要先创建或处理异常
    featured_user = UserFeature.objects.create(userbase=base, context=context, feature_vector=[])
    
    # 拼接字符串，各字段转成字符串，注意部分字段可能为 None
    text = ' '.join([
        str(new_user.age),
        new_user.gender or "",
        str(new_user.height),
        new_user.interests or "",
        new_user.looking_for or "",
        str(new_user.children),
        new_user.education_level or "",
        new_user.occupation or "",
        str(new_user.swiping_history),
        new_user.frequency_of_use or ""
    ])
    
    client_response = client.embeddings.create(input=[text], model=model).data[0].embedding
    featured_user.feature_vector = client_response
    featured_user.save()
    base.preprocessed = True
    base.save()
    return HttpResponse('User processed')

def compute_similarity(user1, user2):
    user1_deature = UserFeature.objects.get(userbase = user1)
    user2_deature = UserFeature.objects.get(userbase = user2)
    return cosine_similarity([user1_deature.feature_vector], [user2_deature.feature_vector])

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