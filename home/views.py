from django.shortcuts import render
from .models import HomeContent

def home(request):
    content = HomeContent.objects.all()
    return render(request, 'home/home.html', {'content': content})
