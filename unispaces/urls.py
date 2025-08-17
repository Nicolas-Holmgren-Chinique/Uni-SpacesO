"""
Main URL Configuration for UniSpaces Project

This is the root URL configuration that routes incoming requests to the
appropriate Django applications within the UniSpaces social networking
platform.

UniSpaces Application Structure:
- Admin interface for site administration
- Home app for landing pages and general content
- Accounts app for user authentication and profile management
- Communities app for creating and managing academic communities

URL Routing Patterns:
- /admin/ -> Django admin interface
- / -> Home app (landing page, about, etc.)
- /accounts/ -> User authentication (login, signup, profile, dashboard)
- /communities/ -> Community management (create, join, manage)

For more information about Django URL patterns:
https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples of URL pattern types:
Function views:
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')

Class-based views:
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')

Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Main URL routing patterns for the UniSpaces application
urlpatterns = [
    # Django Administration Interface
    # ==============================
    # Provides admin interface for managing users, communities, and content
    path('admin/', admin.site.urls),
    
    # Home Application Routes
    # ======================
    # Handles landing page, about page, and general site content
    path('', include('home.urls')),
    
    # Accounts Application Routes
    # ==========================
    # Handles user authentication, registration, profiles, and dashboard
    # Routes: /accounts/login/, /accounts/signup/, /accounts/dashboard/, etc.
    path('accounts/', include('accounts.urls')),
    
    # Communities Application Routes
    # =============================
    # Handles community creation, management, and interaction
    # Routes: /communities/create/, /communities/<slug>/, etc.
    path('communities/', include('communities.urls')),
]

# Media Files Serving (Development Only)
# ======================================
# In development, Django needs to serve user-uploaded media files
# In production, this should be handled by the web server (nginx, Apache)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
