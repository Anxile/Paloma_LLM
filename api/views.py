from django.shortcuts import render, HttpResponse
from openai import OpenAI
from django import settings
client = OpenAI(api_key = settings.OPENAI_API_KEY)


# Create your views here.
def home(request):
    context = {
        'days': [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]
    }
    return render(request, 'profile.html',context)

def submit_form(request):
    user_profile = request.POST.get("username", "Guest")
    return HttpResponse(request)
#     completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {
#             "role": "developer",
#             "content": "Act as an expert matchmaking algorithm with 15 years of experience in behavioral psychology. Perform iterative analysis in 3 phases:\r\n\r\nPhase 1: Hard Filters\r\n- Exclude matches not meeting [min_age], [max_distance], and gender preference from [user_preferences]\r\n- Flag users with >3 common blocked keywords in chat history\r\n\r\nPhase 2: Deep Compatibility Analysis\r\nAnalyze the following dimensions with weights from user's desirability matrix:\r\n1. Lifestyle Synergy (30% weight)\r\n   - Compare [daily_routine] patterns \r\n   - Calculate circadian rhythm overlap using [sleep_schedule] data\r\n   - Map location heatmaps for frequent spots\r\n\r\n2. Value Decoding (40% weight)\r\n   - Semantic analysis on [personal_essay] using LIWC categories\r\n   - Compare moral foundations through [political_views] and [charity_involvement]\r\n   - Detect hidden value conflicts in [social_media_activity] (e.g., environmental activism vs frequent flying)\r\n\r\n3. Growth Potential (30% weight)\r\n   - Identify complementary skill sets from [skills] lists\r\n   - Analyze conflict resolution style through [dispute_scenario_answers]\r\n   - Calculate curiosity overlap using [bucket_list] items\r\n\r\nPhase 3: Match Packaging\r\nFor top 10 candidates:\r\n- Generate 3 personalized icebreakers referencing their [uncommon_interests]\r\n- Predict potential conflict points with mitigation strategies\r\n- Create compatibility timeline: 1-month/1-year/5-year synergy projections\r\n\r\nOutput: JSON with keys:\r\n{\r\n \"matches\": [\r\n   {\r\n     \"user_id\": \"U456\",\r\n     \"compatibility_score\": 0.92,\r\n     \"breakdown\": {\r\n       \"lifestyle\": 0.85,\r\n       \"values\": 0.97,\r\n       \"growth\": 0.88\r\n     },\r\n     \"icebreakers\": [\"I noticed we both want to learn Kintsugi...\"],\r\n     \"risk_factors\": {\"financial_priorities\": 0.3}\r\n   }\r\n ]\r\n}"
#         },
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )
