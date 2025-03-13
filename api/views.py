from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.
def home(request):
    context = {
        'days': [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ],
        'active_hours_in_a_day': [i for i in range(1,8)],
        'cuisines': ['Japanese Cuisine','Indian Cuisine','Canadian Cuisine','Italian Cuisine','Chinese Cuisine','Mexican Cuisine','American Cuisine'],
        'economic_concepts':['Savings','Consumption','Investment','Luxury enthusiasts','Pragmatists','Sharing economy','Independent economy'],
        'personality_and_values':['Extroverted','Introverted','Traditional','Modern','Adventurous','Conservative','Individualism','Collectivism'],
    }
    return render(request, 'profile.html',context)

def submit_form(request):
    if request.method == 'POST':
        try:
            form_data = json.loads(request.body)
            
            about_text = form_data.get('about', '')
            sanitized_about = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', about_text)
            form_data['about'] = sanitized_about
            print(sanitized_about)
        
            available_days = [day for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] if form_data.get(day)]
            cuisines = [cuisine for cuisine in ['Japanese Cuisine', 'Indian Cuisine', 'Canadian Cuisine', 'Italian Cuisine', 'Chinese Cuisine', 'Mexican Cuisine', 'American Cuisine'] if form_data.get(cuisine)]
            economic_concepts = [concept for concept in ['Savings', 'Consumption', 'Investment', 'Luxury enthusiasts', 'Pragmatists', 'Sharing economy', 'Independent economy'] if form_data.get(concept)]
            personality_and_values = [value for value in ['Extroverted', 'Introverted', 'Traditional', 'Modern', 'Adventurous', 'Conservative', 'Individualism', 'Collectivism'] if form_data.get(value)]
        
            simulated_user = {
                "first-name": "Jane",
                "last-name": "Doe",
                "email": "jane.doe@example.com",
                "age": "28",
                "gender": "Female",
                "religion": "None",
                "ethnicity": "Caucasian",
                "JobTitle": "Software Engineer",
                "Industry": "Technology",
                "education": "Bachelor's Degree",
                "about": "I love hiking, reading, and exploring new technologies.",
                "street-address": "1522 Ashland Ave",
                "city": "Niagara Falls",
                "region": "NY",
                "postal-code": "14301",
                "country": "USA",
                "sexualOrientation": "Both",
                "availableDays": ["Monday", "Wednesday", "Friday"],
                "active_hours_in_a_day": "3",
                "cuisines": ["Japanese Cuisine", "Italian Cuisine"],
                "economic_concepts": ["Savings", "Investment"],
                "personality_and_values": ["Extroverted", "Modern", "Adventurous"]
            }


            prompt = (
                f"Act as an expert matchmaking algorithm with 15 years of experience in behavioral psychology. Perform iterative analysis in 3 phases:\n\n"

            
                f"### User 1 Profile Data:\n"
                f"1. **Demographics**:\n"
                f"   - Name: {form_data.get('first-name')} {form_data.get('last-name')}\n"
                f"   - Age: {form_data.get('age')}\n"
                f"   - Gender: {form_data.get('gender')}\n"
                f"   - Ethnicity: {form_data.get('ethnicity')}\n"
                f"   - Religion: {form_data.get('religion')}\n"
                f"   - Sexual Orientation: {form_data.get('sexualOrientation')}\n"
                f"   - Location: {form_data.get('street-address')}, {form_data.get('city')}, {form_data.get('region')}, {form_data.get('postal-code')}, {form_data.get('country')}\n\n"
            
                f"2. **Professional Background**:\n"
                f"   - Job Title: {form_data.get('JobTitle')}\n"
                f"   - Industry: {form_data.get('Industry')}\n"
                f"   - Education: {form_data.get('education')}\n\n"
            
                f"3. **Personal Interests and Lifestyle**:\n"
                f"   - About Me: {sanitized_about}\n"
                f"   - Available Days: {', '.join(available_days)}\n"
                f"   - Spare Hours in a Day: {form_data.get('active_hours_in_a_day')}\n"
                f"   - Favorite Cuisines: {', '.join(cuisines)}\n"
                f"   - Economic Interests: {', '.join(economic_concepts)}\n"
                f"   - Personality and Values: {', '.join(personality_and_values)}\n\n"
            
                f"### Analysis Framework:\n"

                f"### Phase 1: Deep Compatibility Analysis\n"
                f"Analyze the following dimensions with weights from user's desirability matrix:\n"
                f"1. **Lifestyle Synergy (30% weight)**:\n"
                f"   - Compare available_days patterns.\n"
                f"   - Calculate circadian rhythm overlap using active_hours_in_a_day data.\n"
                f"   - Map location heatmaps for frequent spots.\n\n"

                f"2. **Value Decoding (40% weight)**:\n"
                f"   - Compare moral foundations through economic_concepts and personality_and_values.\n"
                f"   - Detect hidden value conflicts in Favorite Cuisines or other preferences (e.g., environmental activism vs frequent flying).\n\n"

                f"3. **Growth Potential (30% weight)**:\n"
                f"   - Identify complementary skill sets from Jobs and industries.\n"
                f"   - Analyze conflict resolution style through Personality and Values.\n"
                f"   - Calculate curiosity overlap using About me.\n\n"

                f"### Phase 2: Match Packaging\n"
                f"For top 10 candidates:\n"
                f"   - Generate 3 personalized icebreakers referencing their profile.\n"
                f"   - Predict potential conflict points with mitigation strategies.\n"
                f"   - Create compatibility timeline: 1-month/1-year/5-year synergy projections.\n\n"
            
                f"User 2:\n"
                f"Name: {simulated_user['first-name']} {simulated_user['last-name']}\n"
                f"Email: {simulated_user['email']}\n"
                f"Age: {simulated_user['age']}\n"
                f"Gender: {simulated_user['gender']}\n"
                f"Religion: {simulated_user['religion']}\n"
                f"Ethnicity: {simulated_user['ethnicity']}\n"
                f"Job Title: {simulated_user['JobTitle']}\n"
                f"Industry: {simulated_user['Industry']}\n"
                f"Education: {simulated_user['education']}\n"
                f"About user: {simulated_user['about']}\n"
                f"Location: {simulated_user['street-address']}, {simulated_user['city']}, {simulated_user['region']}, {simulated_user['postal-code']}, {simulated_user['country']}\n"
                f"Sexual Orientation: {simulated_user['sexualOrientation']}\n"
                f"Available Days: {', '.join(simulated_user['availableDays'])}\n"
                f"Spare Hours in a Day: {simulated_user['active_hours_in_a_day']}\n"
                f"Cuisines: {', '.join(simulated_user['cuisines'])}\n"
                f"Economic Concepts: {', '.join(simulated_user['economic_concepts'])}\n"
                f"Personality and Values: {', '.join(simulated_user['personality_and_values'])}\n"

                f"Please return the analysis in MarkDown format with some necessary Spaces and newlines for reading."
            )
        
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
        
            analysis_result = response.choices[0].message.content.strip()     

            context = {
                'analysis_result': analysis_result
            }
        
            return JsonResponse({'analysis_result': analysis_result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def match_result(request):
    analysis_result = request.GET.get('result', '')
    context = {
        'analysis_result': analysis_result
    }
    return render(request, 'match_result.html', context)