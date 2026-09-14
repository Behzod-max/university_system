from django.contrib import admin
from .models import Teacher, Student, Subject


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "group", "email")
    search_fields = ("first_name", "last_name", "group", "email")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "credits", "teacher")
    search_fields = ("name", "code")
    list_filter = ("teacher",)
    filter_horizontal = ("students",)