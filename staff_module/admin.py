from django.contrib import admin
from .models import RequestSportAchievement, RequestFiles

@admin.register(RequestSportAchievement)
class RequestSportAchievementAdmin(admin.ModelAdmin):
    list_display = ['student']

@admin.register(RequestFiles)
class RequestFilesAdmin(admin.ModelAdmin):
    list_display = ['request', 'uploaded_at']
