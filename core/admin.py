from django.contrib import admin
from .models import StudyGroup, Student, SportCategory, User, Sports, SportAchievement

@admin.register(SportAchievement)
class SportAchievementAdmin(admin.ModelAdmin):
    list_display = ('event',)

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SportCategory)
class SportsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Sports)
class SportsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__email',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)