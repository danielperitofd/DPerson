from django.contrib import admin

from .models import Tenant, TenantMembership


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "plan", "contact_name", "is_active", "created_at")
    list_filter = ("plan", "is_active")
    search_fields = ("name", "slug", "contact_name", "contact_email")


@admin.register(TenantMembership)
class TenantMembershipAdmin(admin.ModelAdmin):
    list_display = ("tenant", "user", "role", "is_default", "is_active")
    list_filter = ("role", "is_default", "is_active")
    search_fields = ("tenant__name", "user__username", "user__full_name")
