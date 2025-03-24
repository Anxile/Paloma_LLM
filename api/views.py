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
            embedding_extract(u)
            return HttpResponse('User created')
        else:
            return HttpResponse('Form is not valid')
    else:
        f = CreateNewUser()
    return render(request, 'create.html', {'form': f})

def user_match(request, userid):
    candidates = []
    user = UserBase.objects.get(id=userid)
    collection = UserBase.objects.all()
    if user.preprocessed:
        for match in collection:
            if match.id == user.id:
                continue
            if not match.preprocessed:
                embedding_extract(User.objects.get(userbase=match))
            sim = compute_similarity(user, match)
            candidates.append((match, sim))
    else:
        embedding_extract(User.objects.get(userbase=user))
    top_candidates = ranking(candidates)
    return render(request, 'match_result.html', {'user': user, 'set': collection, 's': top_candidates})


def embedding_extract(new_user, model="text-embedding-3-small", context="dating"):
    # new_user 是 User 实例，通过外键获取关联的 UserBase 实例
    base = new_user.userbase
    # 获取对应的 UserFeature，注意确保记录存在，否则需要先创建或处理异常
    
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
    featured_user = UserFeature.objects.create(feature_vector = client_response, userbase = base, context = context)
    base.preprocessed = 1
    base.save()
    return HttpResponse('User processed', featured_user)

def compute_similarity(user1, user2):
    user1_deature = UserFeature.objects.get(userbase = user1)
    user2_deature = UserFeature.objects.get(userbase = user2)
    return cosine_similarity([user1_deature.feature_vector], [user2_deature.feature_vector])[0][0]

def ranking(candidates):
    # candidates 为 [(UserBase实例, similarity), ...]
    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return sorted_candidates[:10]

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