from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Tenant, TenantMembership

User = get_user_model()


class TenantForm(forms.ModelForm):
    admin_username = forms.CharField(label="Usuario admin inicial", max_length=150, required=False)
    admin_full_name = forms.CharField(label="Nome do admin inicial", max_length=255, required=False)
    admin_email = forms.EmailField(label="E-mail do admin inicial", required=False)
    admin_whatsapp_phone = forms.CharField(label="WhatsApp do admin inicial", max_length=30, required=False)
    admin_public_sales_contact = forms.BooleanField(label="Usar este admin como contato comercial publico", required=False)
    admin_password = forms.CharField(
        label="Senha do admin inicial",
        required=False,
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Tenant
        fields = [
            "name",
            "slug",
            "contact_name",
            "contact_email",
            "contact_phone",
            "plan",
            "is_active",
            "notes",
            "primary_admin",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["primary_admin"].queryset = User.objects.filter(is_active=True).order_by("username")
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("admin_username")
        password = cleaned.get("admin_password")
        admin_whatsapp_phone = (cleaned.get("admin_whatsapp_phone") or "").strip()
        admin_public_sales_contact = cleaned.get("admin_public_sales_contact")
        if username and User.objects.filter(username=username).exists():
            self.add_error("admin_username", "Ja existe um usuario com esse username.")
        if username and not password:
            self.add_error("admin_password", "Informe a senha do admin inicial.")
        if admin_public_sales_contact and not username:
            self.add_error("admin_username", "Crie um admin inicial para vincular o contato comercial publico.")
        if admin_public_sales_contact and not admin_whatsapp_phone:
            self.add_error("admin_whatsapp_phone", "Informe o WhatsApp do gerente para habilitar o contato publico.")
        return cleaned

    @transaction.atomic
    def save(self, commit=True):
        tenant = super().save(commit=commit)
        username = self.cleaned_data.get("admin_username")
        if username:
            user = User.objects.create_user(
                username=username,
                password=self.cleaned_data["admin_password"],
                email=self.cleaned_data.get("admin_email", ""),
                full_name=self.cleaned_data.get("admin_full_name", ""),
                whatsapp_phone=self.cleaned_data.get("admin_whatsapp_phone", ""),
                is_public_sales_contact=self.cleaned_data.get("admin_public_sales_contact", False),
                role=User.Role.TENANT_ADMIN,
                is_staff=True,
            )
            tenant.primary_admin = user
            tenant.save(update_fields=["primary_admin"])
            TenantMembership.objects.update_or_create(
                tenant=tenant,
                user=user,
                defaults={"role": TenantMembership.Role.ADMIN, "is_default": True, "is_active": True},
            )
        elif tenant.primary_admin:
            TenantMembership.objects.update_or_create(
                tenant=tenant,
                user=tenant.primary_admin,
                defaults={"role": TenantMembership.Role.ADMIN, "is_default": True, "is_active": True},
            )
        return tenant
