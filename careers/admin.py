from django.contrib import admin
from .models import Internship

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'deadline')
    search_fields = ('title', 'company')
