from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Tenant(TimeStampedModel):
    class Plan(models.TextChoices):
        START = "start", "Start"
        PRO = "pro", "Pro"
        TEAM = "team", "Team"
        ENTERPRISE = "enterprise", "Enterprise"

    name = models.CharField("nome", max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    contact_name = models.CharField("responsavel", max_length=150)
    contact_email = models.EmailField("e-mail", blank=True)
    contact_phone = models.CharField("telefone", max_length=30, blank=True)
    plan = models.CharField("plano", max_length=20, choices=Plan.choices, default=Plan.START)
    is_active = models.BooleanField("ativa", default=True)
    notes = models.TextField("observacoes", blank=True)
    primary_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="administered_tenants",
        verbose_name="administrador inicial",
    )

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tenants:list")

    def __str__(self):
        return self.name


class TenantMembership(TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        STAFF = "staff", "Staff"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tenant_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STAFF)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("tenant", "user")
        ordering = ("tenant__name", "user__username")

    def __str__(self):
        return f"{self.user} @ {self.tenant}"
