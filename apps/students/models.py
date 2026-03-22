from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel
from apps.tenants.models import Tenant


class Student(TimeStampedModel):
    class Sex(models.TextChoices):
        FEMALE = "female", "Feminino"
        MALE = "male", "Masculino"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="students")
    full_name = models.CharField("nome completo", max_length=180)
    email = models.EmailField(blank=True)
    phone = models.CharField("telefone", max_length=30, blank=True)
    birth_date = models.DateField("data de nascimento")
    sex = models.CharField("sexo biologico", max_length=10, choices=Sex.choices)
    height_cm = models.DecimalField("altura (cm)", max_digits=5, decimal_places=2)
    objective = models.CharField("objetivo", max_length=255, blank=True)
    notes = models.TextField("observacoes", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("full_name",)
        unique_together = ("tenant", "full_name", "birth_date")

    def get_absolute_url(self):
        return reverse("students:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.full_name
