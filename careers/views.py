from django.shortcuts import render
from .models import Internship

def internship_board(request):
    internships = Internship.objects.all().order_by('-posted_at')
    
    context = {
        'internships': internships,
    }
    return render(request, 'careers/internship_board.html', context)
