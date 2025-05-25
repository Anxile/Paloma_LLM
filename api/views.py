from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import UserBase, User, UserFeature,UserProfile
from .form import CreateNewUser
from sklearn.metrics.pairwise import cosine_similarity

from . import predictor


import joblib

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.

def predict(request, matcher):
        try:
            # --- Fetch profile data from your database/models ---
            matcher_obj = UserProfile.objects.get(uuid=matcher)


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

            
            ranking = []

            for matchee in UserProfile.objects.all():
                profile2_data = {
                    'gender': matchee.gender,
                    'degree': matchee.degree,
                    'children': matchee.children,
                    'relationship_status': matchee.relationship_status,
                    'politics': matchee.politics,
                    'religion': matchee.religion,
                    'substances_alcohol': matchee.substances_alcohol,
                    'substances_cannabis': matchee.substances_cannabis,
                    'substances_nicotine': matchee.substances_nicotine,
                    'age_importance': matchee.age_importance,
                    'degree_importance': matchee.degree_importance,
                    'children_importance': matchee.children_importance,
                    'ethnicity_importance': matchee.ethnicity_importance,
                    'politics_importance': matchee.politics_importance,
                    'religion_importance': matchee.religion_importance,
                    'height_importance': matchee.height_importance,
                    'age_expected_lower_bound': matchee.age_expected_lower_bound,
                    'age_expected_upper_bound': matchee.age_expected_upper_bound,
                }
                ranking.append(predictor.predict_match_probability_full(profile1_data, profile2_data))
            ranking.sort(reverse=True)
            
            return JsonResponse({'ranking': ranking})

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
                
def predict_one_on_one(request, matcher, matchee):
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







def compute_similarity(user1, user2):
    user1_feature = UserFeature.objects.get(userbase = user1)
    user2_feature = UserFeature.objects.get(userbase = user2)
    return cosine_similarity([user1_feature.feature_vector], [user2_feature.feature_vector])[0][0]

def ranking(candidates):
    # candidates: [(UserBase instances, similarity), ...]
    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return sorted_candidates[:10]
