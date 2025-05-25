from user.models.user_base import UserBase
from user.models.user import User
from user.seeds.data_seed import UserData
from django.http import JsonResponse


def seedUserData():
    user_data = UserData.data

    count = 0
    
    for item in user_data:
        user_base_name = f"User_{item.get('User ID')}"
        
        try:
            try:
                user_base = UserBase.objects.get(name=user_base_name)
            except UserBase.DoesNotExist:
                user_base = UserBase.objects.create(name=user_base_name, preprocessed=False)
            
            User.objects.create(
                userbase=user_base,
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
    
    return JsonResponse({"message":"Created {count} users out of {len(user_data)}"}, status=200)