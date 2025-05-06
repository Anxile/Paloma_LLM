from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import UserBase, User, UserFeature,UserProfile
from .form import CreateNewUser
from .data_seed import UserData
from sklearn.metrics.pairwise import cosine_similarity

from . import predictor


import joblib

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.

def predict(request, matcher, matchee):
        try:
            # --- Fetch profile data from your database/models ---
            matcher_obj = UserProfile.objects.get(uuid=matcher)
            matchee_obj = UserProfile.objects.get(uuid=matchee)


            profile1_data = {
                'gender': matcher_obj.gender,
                'degree': matcher_obj.degree,
                'children': matcher_obj.children,
                'relationship_status': matcher_obj.relationship_status,
                'politics': matcher_obj.politics,
                'religion': matcher_obj.religion,
                'substances_alcohol': matcher_obj.substances_alcohol,
                'substances_cannabis': matcher_obj.substances_cannabis,
                'substances_nicotine': matcher_obj.substances_nicotine,
                'age_importance': matcher_obj.age_importance,
                'degree_importance': matcher_obj.degree_importance,
                'children_importance': matcher_obj.children_importance,
                'ethnicity_importance': matcher_obj.ethnicity_importance,
                'politics_importance': matcher_obj.politics_importance,
                'religion_importance': matcher_obj.religion_importance,
                'height_importance': matcher_obj.height_importance,
                'age_expected_lower_bound': matcher_obj.age_expected_lower_bound,
                'age_expected_upper_bound': matcher_obj.age_expected_upper_bound,
            }
            profile2_data = {
                'gender': matchee_obj.gender,
                'degree': matchee_obj.degree,
                'children': matchee_obj.children,
                'relationship_status': matchee_obj.relationship_status,
                'politics': matchee_obj.politics,
                'religion': matchee_obj.religion,
                'substances_alcohol': matchee_obj.substances_alcohol,
                'substances_cannabis': matchee_obj.substances_cannabis,
                'substances_nicotine': matchee_obj.substances_nicotine,
                'age_importance': matchee_obj.age_importance,
                'degree_importance': matchee_obj.degree_importance,
                'children_importance': matchee_obj.children_importance,
                'ethnicity_importance': matchee_obj.ethnicity_importance,
                'politics_importance': matchee_obj.politics_importance,
                'religion_importance': matchee_obj.religion_importance,
                'height_importance': matchee_obj.height_importance,
                'age_expected_lower_bound': matchee_obj.age_expected_lower_bound,
                'age_expected_upper_bound': matchee_obj.age_expected_upper_bound,
           }

            # Call the predictor function for the full model
            probability = predictor.predict_match_probability_full(profile1_data, profile2_data)

            if probability >= 0:
                return JsonResponse({'matcher': matcher,
                                     'matchee': matchee,
                                     'match_probability': probability})
            else:
                return JsonResponse({'error': 'Prediction failed internally.'}, status=500)

        except UserProfile.DoesNotExist:
             return JsonResponse({'error': 'One or both profiles not found.'}, status=404)
        except KeyError as e:
             # This might happen if profile_data dict is missing keys needed by predictor
             return JsonResponse({'error': f'Missing profile data key: {e}'}, status=400)
        except ValueError as e:
             # This might happen during preprocessing in the predictor
             return JsonResponse({'error': f'Data processing error: {e}'}, status=400)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
                



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
    return render(request, 'match_result.html', {'user': user, 'candidates': top_candidates})


def embedding_extract(new_user, model="text-embedding-3-small", context="dating"):
    base = new_user.userbase
    
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
    user1_feature = UserFeature.objects.get(userbase = user1)
    user2_feature = UserFeature.objects.get(userbase = user2)
    return cosine_similarity([user1_feature.feature_vector], [user2_feature.feature_vector])[0][0]

def ranking(candidates):
    # candidates: [(UserBase instances, similarity), ...]
    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return sorted_candidates[:10]

def test_cosine_similarity(request):
    text1 = request.GET.get('text1', '')
    text2 = request.GET.get('text2', '')

    if not text1 or not text2:
        return HttpResponse("Missing parameters", status=400)

    response1 = client.embeddings.create(input=[text1], model="text-embedding-3-small").data[0].embedding
    response2 = client.embeddings.create(input=[text2], model="text-embedding-3-small").data[0].embedding

    similarity = cosine_similarity([response1], [response2])[0][0]
    return HttpResponse(similarity)

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