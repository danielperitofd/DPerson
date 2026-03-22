from django import forms

from apps.students.models import Student

from .models import PhysicalAssessment, PosturalAssessment


class TenantStudentMixin:
    def __init__(self, *args, tenant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if "student" in self.fields and tenant is not None:
            self.fields["student"].queryset = Student.objects.filter(tenant=tenant, is_active=True).order_by("full_name")
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class PhysicalAssessmentForm(TenantStudentMixin, forms.ModelForm):
    class Meta:
        model = PhysicalAssessment
        exclude = ("tenant", "bmi", "bmi_classification", "waist_hip_ratio", "body_fat_percentage", "fat_mass_kg", "lean_mass_kg", "ideal_weight_kg")
        widgets = {
            "assessed_at": forms.DateInput(attrs={"type": "date"}),
            "observations": forms.Textarea(attrs={"rows": 4}),
        }


class PosturalAssessmentForm(TenantStudentMixin, forms.ModelForm):
    class Meta:
        model = PosturalAssessment
        exclude = ("tenant",)
        widgets = {
            "assessed_at": forms.DateInput(attrs={"type": "date"}),
            "lateral_view": forms.Textarea(attrs={"rows": 3}),
            "anterior_view": forms.Textarea(attrs={"rows": 3}),
            "posterior_view": forms.Textarea(attrs={"rows": 3}),
            "markings": forms.Textarea(attrs={"rows": 3}),
            "observations": forms.Textarea(attrs={"rows": 3}),
        }
