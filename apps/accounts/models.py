from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MASTER = "master", "Master"
        TENANT_ADMIN = "tenant_admin", "Administrador da Tenant"
        TENANT_STAFF = "tenant_staff", "Staff da Tenant"

    full_name = models.CharField("nome completo", max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TENANT_STAFF)
    must_change_password = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.full_name and not self.first_name and not self.last_name:
            parts = self.full_name.split(" ", 1)
            self.first_name = parts[0]
            if len(parts) > 1:
                self.last_name = parts[1]
        super().save(*args, **kwargs)

    @property
    def is_master(self):
        return self.is_superuser or self.role == self.Role.MASTER

    def __str__(self):
        return self.full_name or self.get_full_name() or self.username
