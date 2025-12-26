from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.library_home, name='home'),
    path('search/', views.search_books, name='search'),
    path('upload/', views.upload_material, name='upload'),
]
