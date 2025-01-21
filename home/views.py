from django.shortcuts import render
from .models import HomeContent

def home(request):
    content = HomeContent.objects.filter(type='home')
    base_content = HomeContent.objects.filter(type='base') 
    return render(request, 'home/home.html', {'content': content, 'base_content': base_content})
