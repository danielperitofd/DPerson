from django.contrib import admin

from .models import PhysicalAssessment, PosturalAssessment


@admin.register(PhysicalAssessment)
class PhysicalAssessmentAdmin(admin.ModelAdmin):
    list_display = ("student", "tenant", "assessed_at", "bmi", "body_fat_percentage")
    list_filter = ("tenant", "protocol")
    search_fields = ("student__full_name",)


@admin.register(PosturalAssessment)
class PosturalAssessmentAdmin(admin.ModelAdmin):
    list_display = ("student", "tenant", "assessed_at", "photo_upload_ready")
    list_filter = ("tenant", "photo_upload_ready")
    search_fields = ("student__full_name",)
