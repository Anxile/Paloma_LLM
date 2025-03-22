from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import UserCollection, User

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.

def home(request):
    members = {'name':'Yihe', 'sex':'male'}
    return render(request, 'home.html', members)

def user_match(request, userid):
    item = UserCollection.objects.all()

    user = UserCollection.objects.get(id=userid)


    return render(request, 'todo_test.html', {'user': user})