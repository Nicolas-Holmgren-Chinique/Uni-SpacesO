from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('mission-control/', views.internship_board, name='mission_control'),
]
