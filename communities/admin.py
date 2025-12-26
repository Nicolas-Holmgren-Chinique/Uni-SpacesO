from django.contrib import admin
from .models import Community, Membership
from .project_models import Project, Skill

# Register your models here.

admin.site.register(Community)
admin.site.register(Membership)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('skills', 'collaborators')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)