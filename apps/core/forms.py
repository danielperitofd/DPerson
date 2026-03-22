from django import forms

from .models import PublicLead


class PublicLeadForm(forms.ModelForm):
    class Meta:
        model = PublicLead
        fields = ("name", "email", "phone", "company_name", "plan_interest", "message")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Conte um pouco da sua operacao, objetivo comercial ou numero de alunos."}),
        }
        labels = {
            "company_name": "Empresa ou marca",
            "plan_interest": "Plano de interesse",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Seu nome"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "seuemail@dominio.com"})
        self.fields["phone"].widget.attrs.update({"class": "form-control", "placeholder": "WhatsApp ou telefone"})
        self.fields["company_name"].widget.attrs.update({"class": "form-control", "placeholder": "Nome do estudio, equipe ou marca"})
        self.fields["plan_interest"].widget = forms.Select(
            choices=[
                ("start", "Start"),
                ("pro", "Pro"),
                ("team", "Team"),
                ("enterprise", "Enterprise"),
            ],
            attrs={"class": "form-select"},
        )
        self.fields["message"].widget.attrs.update({"class": "form-control"})
