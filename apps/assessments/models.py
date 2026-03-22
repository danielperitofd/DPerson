from django.db import models
from django.urls import reverse

from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.tenants.models import Tenant

from .services import calculate_bmi, calculate_body_fat_percentage, calculate_composition, calculate_waist_hip_ratio, classify_bmi


class PhysicalAssessment(TimeStampedModel):
    class Protocol(models.TextChoices):
        JACKSON_POLLOCK = "jackson_pollock", "Jackson & Pollock"
        FAULKNER = "faulkner", "Faulkner"
        CUSTOM = "custom", "Personalizado"

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="physical_assessments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="physical_assessments")
    assessed_at = models.DateField("data da avaliacao")
    age = models.PositiveIntegerField("idade")
    weight_kg = models.DecimalField("peso (kg)", max_digits=6, decimal_places=2)
    height_cm = models.DecimalField("altura (cm)", max_digits=5, decimal_places=2)
    target_fat_percentage = models.DecimalField("meta de gordura (%)", max_digits=5, decimal_places=2, null=True, blank=True)
    protocol = models.CharField("protocolo", max_length=40, choices=Protocol.choices, default=Protocol.JACKSON_POLLOCK)
    waist_cm = models.DecimalField("cintura (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    hip_cm = models.DecimalField("quadril (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    chest_skinfold_mm = models.DecimalField("dobra peitoral (mm)", max_digits=5, decimal_places=2, null=True, blank=True)
    abdomen_skinfold_mm = models.DecimalField("dobra abdominal (mm)", max_digits=5, decimal_places=2, null=True, blank=True)
    thigh_skinfold_mm = models.DecimalField("dobra coxa (mm)", max_digits=5, decimal_places=2, null=True, blank=True)
    tricep_skinfold_mm = models.DecimalField("dobra triceps (mm)", max_digits=5, decimal_places=2, null=True, blank=True)
    suprailiac_skinfold_mm = models.DecimalField("dobra supra-iliaca (mm)", max_digits=5, decimal_places=2, null=True, blank=True)
    humerus_diameter_cm = models.DecimalField("diametro do umero (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    femur_diameter_cm = models.DecimalField("diametro do femur (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    arm_circumference_cm = models.DecimalField("perimetro braco (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    thigh_circumference_cm = models.DecimalField("perimetro coxa (cm)", max_digits=5, decimal_places=2, null=True, blank=True)
    pushups_reps = models.PositiveIntegerField("flexoes", null=True, blank=True)
    plank_seconds = models.PositiveIntegerField("prancha (s)", null=True, blank=True)
    cooper_distance_m = models.PositiveIntegerField("Cooper 12min (m)", null=True, blank=True)
    observations = models.TextField("observacoes", blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bmi_classification = models.CharField(max_length=50, blank=True)
    waist_hip_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat_mass_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    lean_mass_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ideal_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ("-assessed_at", "-created_at")

    def save(self, *args, **kwargs):
        self.bmi = calculate_bmi(self.weight_kg, self.height_cm)
        self.bmi_classification = classify_bmi(self.bmi)
        self.waist_hip_ratio = calculate_waist_hip_ratio(self.waist_cm, self.hip_cm)
        self.body_fat_percentage = calculate_body_fat_percentage(
            self.student.sex,
            self.age,
            self.chest_skinfold_mm,
            self.abdomen_skinfold_mm,
            self.thigh_skinfold_mm,
            self.tricep_skinfold_mm,
            self.suprailiac_skinfold_mm,
        )
        fat_mass, lean_mass, ideal_weight = calculate_composition(
            self.weight_kg,
            self.body_fat_percentage,
            self.target_fat_percentage,
        )
        self.fat_mass_kg = fat_mass
        self.lean_mass_kg = lean_mass
        self.ideal_weight_kg = ideal_weight
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("assessments:physical_list")

    def __str__(self):
        return f"{self.student} - {self.assessed_at}"


class PosturalAssessment(TimeStampedModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="postural_assessments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="postural_assessments")
    assessed_at = models.DateField("data da avaliacao")
    lateral_view = models.TextField("vista lateral", blank=True)
    anterior_view = models.TextField("vista anterior", blank=True)
    posterior_view = models.TextField("vista posterior", blank=True)
    markings = models.TextField("marcacoes", blank=True)
    observations = models.TextField("observacoes", blank=True)
    photo_upload_ready = models.BooleanField(default=True)

    class Meta:
        ordering = ("-assessed_at", "-created_at")

    def get_absolute_url(self):
        return reverse("assessments:postural_list")

    def __str__(self):
        return f"Postural {self.student} - {self.assessed_at}"
