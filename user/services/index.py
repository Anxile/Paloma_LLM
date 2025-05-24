from django.shortcuts import render
from django.http import HttpResponse
from user.models import UserBase

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