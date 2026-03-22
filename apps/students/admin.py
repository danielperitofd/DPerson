from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "tenant", "phone", "birth_date", "is_active")
    list_filter = ("tenant", "sex", "is_active")
    search_fields = ("full_name", "email", "phone")
