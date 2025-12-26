from django.contrib import admin
from .models import Subject, Textbook, StudyMaterial

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subject', 'provider')
    list_filter = ('subject', 'provider')
    search_fields = ('title', 'author', 'isbn')

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'subject', 'material_type', 'downloads')
    list_filter = ('subject', 'material_type')
    search_fields = ('title', 'description')
