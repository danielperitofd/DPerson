from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from apps.tenants.models import TenantMembership

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Seu usuario"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Sua senha"}),
    )


class TenantUserForm(forms.ModelForm):
    membership_role = forms.ChoiceField(label="Perfil da tenant", choices=TenantMembership.Role.choices)
    password = forms.CharField(label="Senha inicial", required=False, widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(label="Confirmar senha", required=False, widget=forms.PasswordInput(render_value=True))
    is_active = forms.BooleanField(label="Usuario ativo", required=False, initial=True)

    class Meta:
        model = User
        fields = ("username", "full_name", "email", "is_active")

    def __init__(self, *args, membership=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.membership = membership
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"
        if membership:
            self.fields["membership_role"].initial = membership.role
        if self.instance.pk:
            self.fields["password"].help_text = "Opcional. Preencha apenas se quiser redefinir a senha."

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")
        if self.instance.pk:
            if password and password != confirm_password:
                self.add_error("confirm_password", "As senhas nao conferem.")
        else:
            if not password:
                self.add_error("password", "Informe a senha inicial.")
            if password != confirm_password:
                self.add_error("confirm_password", "As senhas nao conferem.")
        return cleaned

    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ja existe um usuario com esse username.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        membership_role = self.cleaned_data["membership_role"]
        user.role = User.Role.TENANT_ADMIN if membership_role == TenantMembership.Role.ADMIN else User.Role.TENANT_STAFF
        user.is_staff = True
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
