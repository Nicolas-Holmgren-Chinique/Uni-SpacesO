from django.contrib.auth import views as auth_views
from django.urls import path
from .views import CustomLoginView, DashboardView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Ensure this points to your dashboard view
]