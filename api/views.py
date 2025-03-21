from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
import re
from .models import TodoItem

client = OpenAI(api_key = settings.OPENAI_API_KEY)

# Create your views here.

def home(request):
    members = {'name':'Yihe', 'sex':'male'}
    return render(request, 'profile.html', members)

def todo(request):
    item = TodoItem.objects.all()
    return render(request, 'todo.html', {'item': item})