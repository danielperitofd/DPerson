from django.contrib import admin

from .models import PublicLead


@admin.register(PublicLead)
class PublicLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "plan_interest", "status", "created_at")
    list_filter = ("plan_interest", "status", "created_at")
    search_fields = ("name", "email", "phone", "company_name")
