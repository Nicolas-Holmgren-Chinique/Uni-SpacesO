from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render
from django.urls import reverse_lazy

# from .forms import LoginForm, SignUpForm
from django.views.generic import CreateView


# Create your views here.

"""
Here is the login view, for our login form."""

# class LoginView(FormView):

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Path to your login template
    redirect_authenticated_user = True  # Redirect if user is already authenticated
    authentication_form = AuthenticationForm  # Use Django's built-in AuthenticationForm


# dashboard was missplelled lets see if fixing it works

    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redirect to the dashboard after login


"""
Here is the signup view, for our signup form.
we use the UserCreationForm from django.contrib.auth.forms
to create a form for the user to sign up.

we then use the CreateView generic view to display the form

the template_name is the path to the template file that will be used to render the form and the 
success_url is the path to redirect to after the form is successfully submitted.
"""

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')



"""
Here is the dashboard view, which is the main page after login.
we use the login_required decorator to ensure that only authenticated users can access this view."""


@login_required 
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'} # You can pass any context variables you need here
    )


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'  # Path to your dashboard template