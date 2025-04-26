from django.contrib.auth import views as auth_views
from django.urls import path
from .views import CustomLoginView, DashboardView, SignUpView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),  # Ensure this points to your signup view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Ensure this points to your dashboard view
]


"""
Note to my self, I am working on the sign up, so far template and urls are done
I next need to work on the model and the view for the sign up, then test it out.
"""