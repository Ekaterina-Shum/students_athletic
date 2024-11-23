from django.contrib import admin
from .models import StudyGroup, Student, User

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'curator')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__email',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)