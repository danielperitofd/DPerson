from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublicLead(TimeStampedModel):
    class PlanInterest(models.TextChoices):
        START = "start", "Start"
        PRO = "pro", "Pro"
        TEAM = "team", "Team"
        ENTERPRISE = "enterprise", "Enterprise"

    class Status(models.TextChoices):
        NEW = "new", "Novo"
        CONTACTED = "contacted", "Contatado"
        QUALIFIED = "qualified", "Qualificado"
        CLOSED = "closed", "Fechado"

    name = models.CharField("nome", max_length=150)
    email = models.EmailField("e-mail")
    phone = models.CharField("telefone", max_length=30)
    company_name = models.CharField("empresa", max_length=150, blank=True)
    plan_interest = models.CharField("plano de interesse", max_length=30, choices=PlanInterest.choices)
    message = models.TextField("mensagem", blank=True)
    status = models.CharField("status", max_length=20, choices=Status.choices, default=Status.NEW)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "lead publico"
        verbose_name_plural = "leads publicos"

    def __str__(self):
        return f"{self.name} - {self.get_plan_interest_display()}"
