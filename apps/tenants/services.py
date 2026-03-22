from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction

from apps.assessments.models import PhysicalAssessment, PosturalAssessment
from apps.students.models import Student

from .models import Tenant, TenantMembership

User = get_user_model()

SEED_NOTE = "[seed:test-data]"
SEED_PASSWORD = "Seed@123"
LEGACY_SEED_SLUGS = ["seed-davi-alves-performance"]
LEGACY_SEED_USERNAMES = ["seed_admin_davi", "seed_staff_davi"]

SEED_PROFILES = {
    "iniciante": {
        "label": "Avaliacao Iniciante",
        "tenant_slug": "seed-avaliacao-iniciante",
        "tenant_name": "Seed Avaliacao Iniciante",
        "contact_name": "Davi Alves",
        "plan": Tenant.Plan.START,
        "admin_username": "seed_iniciante_admin",
        "staff_username": "seed_iniciante_staff",
        "student": {
            "full_name": "Mariana Costa Ribeiro",
            "birth_date": date(1998, 4, 12),
            "email": "mariana.iniciante@test.local",
            "phone": "(11) 97777-1101",
            "sex": Student.Sex.FEMALE,
            "height_cm": Decimal("165.00"),
            "objective": "Iniciar rotina de treinos, ganhar consistencia e melhorar condicionamento geral.",
            "notes": "Perfil iniciante com foco em adaptacao e aderencia.",
        },
        "physical": [
            {
                "assessed_at": date(2026, 1, 8),
                "age": 27,
                "weight_kg": Decimal("71.20"),
                "height_cm": Decimal("165.00"),
                "target_fat_percentage": Decimal("24.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("83.00"),
                "hip_cm": Decimal("103.00"),
                "chest_skinfold_mm": Decimal("0.00"),
                "abdomen_skinfold_mm": Decimal("0.00"),
                "thigh_skinfold_mm": Decimal("28.00"),
                "tricep_skinfold_mm": Decimal("24.00"),
                "suprailiac_skinfold_mm": Decimal("21.00"),
                "humerus_diameter_cm": Decimal("6.40"),
                "femur_diameter_cm": Decimal("8.80"),
                "arm_circumference_cm": Decimal("30.50"),
                "thigh_circumference_cm": Decimal("57.20"),
                "pushups_reps": 8,
                "plank_seconds": 24,
                "cooper_distance_m": 1450,
                "observations": "Primeira avaliacao funcional e corporal da aluna. [seed:test-data]",
            },
            {
                "assessed_at": date(2026, 3, 5),
                "age": 27,
                "weight_kg": Decimal("69.80"),
                "height_cm": Decimal("165.00"),
                "target_fat_percentage": Decimal("24.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("80.00"),
                "hip_cm": Decimal("101.00"),
                "chest_skinfold_mm": Decimal("0.00"),
                "abdomen_skinfold_mm": Decimal("0.00"),
                "thigh_skinfold_mm": Decimal("25.00"),
                "tricep_skinfold_mm": Decimal("21.00"),
                "suprailiac_skinfold_mm": Decimal("19.00"),
                "humerus_diameter_cm": Decimal("6.40"),
                "femur_diameter_cm": Decimal("8.80"),
                "arm_circumference_cm": Decimal("31.20"),
                "thigh_circumference_cm": Decimal("56.40"),
                "pushups_reps": 14,
                "plank_seconds": 43,
                "cooper_distance_m": 1680,
                "observations": "Evolucao inicial positiva em aderencia e resistencia. [seed:test-data]",
            },
        ],
        "postural": {
            "assessed_at": date(2026, 3, 5),
            "lateral_view": "Leve anteriorizacao de cabeca e tendencia a retroversao pelvica em repouso.",
            "anterior_view": "Assimetria discreta de ombros e joelhos em valgo leve.",
            "posterior_view": "Escapulas relativamente estaveis, com pequena assimetria de altura.",
            "markings": "Trabalhar mobilidade de tornozelo, quadril e consciencia corporal.",
            "observations": "Perfil ideal para onboarding e demonstracao de progresso inicial. [seed:test-data]",
            "photo_upload_ready": True,
        },
    },
    "emagrecimento": {
        "label": "Emagrecimento",
        "tenant_slug": "seed-emagrecimento",
        "tenant_name": "Seed Emagrecimento",
        "contact_name": "Davi Alves",
        "plan": Tenant.Plan.PRO,
        "admin_username": "seed_emag_admin",
        "staff_username": "seed_emag_staff",
        "student": {
            "full_name": "Carlos Eduardo Gomes",
            "birth_date": date(1992, 8, 17),
            "email": "carlos.eduardo@test.local",
            "phone": "(11) 98888-1122",
            "sex": Student.Sex.MALE,
            "height_cm": Decimal("178.00"),
            "objective": "Reducao de gordura, melhora postural e ganho de condicionamento.",
            "notes": "Perfil inspirado na estrutura do relatorio profissional. [seed:test-data]",
        },
        "physical": [
            {
                "assessed_at": date(2025, 12, 5),
                "age": 33,
                "weight_kg": Decimal("92.40"),
                "height_cm": Decimal("178.00"),
                "target_fat_percentage": Decimal("14.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("95.00"),
                "hip_cm": Decimal("101.00"),
                "chest_skinfold_mm": Decimal("14.00"),
                "abdomen_skinfold_mm": Decimal("28.00"),
                "thigh_skinfold_mm": Decimal("20.00"),
                "tricep_skinfold_mm": Decimal("11.00"),
                "suprailiac_skinfold_mm": Decimal("19.00"),
                "humerus_diameter_cm": Decimal("7.10"),
                "femur_diameter_cm": Decimal("9.60"),
                "arm_circumference_cm": Decimal("36.20"),
                "thigh_circumference_cm": Decimal("59.80"),
                "pushups_reps": 26,
                "plank_seconds": 58,
                "cooper_distance_m": 2100,
                "observations": "Primeira coleta de referencia corporal. [seed:test-data]",
            },
            {
                "assessed_at": date(2026, 1, 16),
                "age": 33,
                "weight_kg": Decimal("89.10"),
                "height_cm": Decimal("178.00"),
                "target_fat_percentage": Decimal("14.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("91.50"),
                "hip_cm": Decimal("100.00"),
                "chest_skinfold_mm": Decimal("12.00"),
                "abdomen_skinfold_mm": Decimal("24.00"),
                "thigh_skinfold_mm": Decimal("18.00"),
                "tricep_skinfold_mm": Decimal("10.00"),
                "suprailiac_skinfold_mm": Decimal("17.00"),
                "humerus_diameter_cm": Decimal("7.10"),
                "femur_diameter_cm": Decimal("9.60"),
                "arm_circumference_cm": Decimal("37.00"),
                "thigh_circumference_cm": Decimal("58.90"),
                "pushups_reps": 33,
                "plank_seconds": 74,
                "cooper_distance_m": 2320,
                "observations": "Melhora de composicao corporal e resistencia. [seed:test-data]",
            },
            {
                "assessed_at": date(2026, 2, 28),
                "age": 33,
                "weight_kg": Decimal("86.70"),
                "height_cm": Decimal("178.00"),
                "target_fat_percentage": Decimal("14.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("88.20"),
                "hip_cm": Decimal("98.80"),
                "chest_skinfold_mm": Decimal("10.00"),
                "abdomen_skinfold_mm": Decimal("19.00"),
                "thigh_skinfold_mm": Decimal("16.00"),
                "tricep_skinfold_mm": Decimal("9.00"),
                "suprailiac_skinfold_mm": Decimal("14.00"),
                "humerus_diameter_cm": Decimal("7.10"),
                "femur_diameter_cm": Decimal("9.60"),
                "arm_circumference_cm": Decimal("37.50"),
                "thigh_circumference_cm": Decimal("58.40"),
                "pushups_reps": 41,
                "plank_seconds": 96,
                "cooper_distance_m": 2550,
                "observations": "Etapa de consolidacao de performance e reducao de gordura. [seed:test-data]",
            },
        ],
        "postural": {
            "assessed_at": date(2026, 2, 28),
            "lateral_view": "Cabeca anteriorizada leve, discreto aumento de cifose toracica.",
            "anterior_view": "Assimetria suave de ombros e rotacao interna moderada de ombro direito.",
            "posterior_view": "Escapulas com leve abducao, quadril estavel e apoio plantar simetrico.",
            "markings": "Priorizar mobilidade toracica, controle escapular e fortalecimento de gluteos.",
            "observations": "Avaliacao postural para jornada de reducao de gordura. [seed:test-data]",
            "photo_upload_ready": True,
        },
    },
    "hipertrofia": {
        "label": "Hipertrofia",
        "tenant_slug": "seed-hipertrofia",
        "tenant_name": "Seed Hipertrofia",
        "contact_name": "Davi Alves",
        "plan": Tenant.Plan.TEAM,
        "admin_username": "seed_hiper_admin",
        "staff_username": "seed_hiper_staff",
        "student": {
            "full_name": "Lucas Henrique Prado",
            "birth_date": date(1995, 11, 3),
            "email": "lucas.hipertrofia@test.local",
            "phone": "(11) 96666-2211",
            "sex": Student.Sex.MALE,
            "height_cm": Decimal("182.00"),
            "objective": "Ganho de massa magra com manutencao do percentual de gordura controlado.",
            "notes": "Perfil pensado para vender consultoria de performance e composicao corporal. [seed:test-data]",
        },
        "physical": [
            {
                "assessed_at": date(2025, 11, 20),
                "age": 30,
                "weight_kg": Decimal("78.40"),
                "height_cm": Decimal("182.00"),
                "target_fat_percentage": Decimal("11.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("80.00"),
                "hip_cm": Decimal("97.00"),
                "chest_skinfold_mm": Decimal("8.00"),
                "abdomen_skinfold_mm": Decimal("12.00"),
                "thigh_skinfold_mm": Decimal("10.00"),
                "tricep_skinfold_mm": Decimal("7.00"),
                "suprailiac_skinfold_mm": Decimal("8.00"),
                "humerus_diameter_cm": Decimal("7.40"),
                "femur_diameter_cm": Decimal("9.90"),
                "arm_circumference_cm": Decimal("37.80"),
                "thigh_circumference_cm": Decimal("58.00"),
                "pushups_reps": 36,
                "plank_seconds": 88,
                "cooper_distance_m": 2480,
                "observations": "Base seca para fase de superavit controlado. [seed:test-data]",
            },
            {
                "assessed_at": date(2026, 1, 15),
                "age": 30,
                "weight_kg": Decimal("81.10"),
                "height_cm": Decimal("182.00"),
                "target_fat_percentage": Decimal("11.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("81.20"),
                "hip_cm": Decimal("98.00"),
                "chest_skinfold_mm": Decimal("8.00"),
                "abdomen_skinfold_mm": Decimal("13.00"),
                "thigh_skinfold_mm": Decimal("11.00"),
                "tricep_skinfold_mm": Decimal("7.00"),
                "suprailiac_skinfold_mm": Decimal("8.00"),
                "humerus_diameter_cm": Decimal("7.40"),
                "femur_diameter_cm": Decimal("9.90"),
                "arm_circumference_cm": Decimal("39.10"),
                "thigh_circumference_cm": Decimal("59.20"),
                "pushups_reps": 40,
                "plank_seconds": 96,
                "cooper_distance_m": 2520,
                "observations": "Ganho de massa com estabilidade de cintura. [seed:test-data]",
            },
            {
                "assessed_at": date(2026, 3, 1),
                "age": 30,
                "weight_kg": Decimal("83.00"),
                "height_cm": Decimal("182.00"),
                "target_fat_percentage": Decimal("11.00"),
                "protocol": PhysicalAssessment.Protocol.JACKSON_POLLOCK,
                "waist_cm": Decimal("82.00"),
                "hip_cm": Decimal("99.20"),
                "chest_skinfold_mm": Decimal("9.00"),
                "abdomen_skinfold_mm": Decimal("14.00"),
                "thigh_skinfold_mm": Decimal("11.00"),
                "tricep_skinfold_mm": Decimal("8.00"),
                "suprailiac_skinfold_mm": Decimal("9.00"),
                "humerus_diameter_cm": Decimal("7.40"),
                "femur_diameter_cm": Decimal("9.90"),
                "arm_circumference_cm": Decimal("40.00"),
                "thigh_circumference_cm": Decimal("60.00"),
                "pushups_reps": 44,
                "plank_seconds": 104,
                "cooper_distance_m": 2580,
                "observations": "Perfil ideal para storytelling de hipertrofia no dashboard. [seed:test-data]",
            },
        ],
        "postural": {
            "assessed_at": date(2026, 3, 1),
            "lateral_view": "Boa organizacao geral com tendencia a extensao lombar em repouso.",
            "anterior_view": "Membros superiores simetricos e pe direito com discreta rotacao externa.",
            "posterior_view": "Escapulas estaveis, com elevacao minima no lado dominante.",
            "markings": "Monitorar controle de core e padrao respiratorio durante cargas altas.",
            "observations": "Base postural para atleta recreativo em fase de massa. [seed:test-data]",
            "photo_upload_ready": True,
        },
    },
    "reabilitacao_postural": {
        "label": "Reabilitacao Postural",
        "tenant_slug": "seed-reabilitacao-postural",
        "tenant_name": "Seed Reabilitacao Postural",
        "contact_name": "Davi Alves",
        "plan": Tenant.Plan.PRO,
        "admin_username": "seed_reab_admin",
        "staff_username": "seed_reab_staff",
        "student": {
            "full_name": "Fernanda Araujo Lima",
            "birth_date": date(1989, 2, 9),
            "email": "fernanda.reab@test.local",
            "phone": "(11) 95555-3301",
            "sex": Student.Sex.FEMALE,
            "height_cm": Decimal("168.00"),
            "objective": "Diminuir dores lombares e corrigir compensacoes posturais do trabalho sentado.",
            "notes": "Perfil orientado a postural e acompanhamento funcional. [seed:test-data]",
        },
        "physical": [
            {
                "assessed_at": date(2025, 12, 12),
                "age": 37,
                "weight_kg": Decimal("74.50"),
                "height_cm": Decimal("168.00"),
                "target_fat_percentage": Decimal("23.00"),
                "protocol": PhysicalAssessment.Protocol.CUSTOM,
                "waist_cm": Decimal("84.00"),
                "hip_cm": Decimal("101.00"),
                "chest_skinfold_mm": Decimal("0.00"),
                "abdomen_skinfold_mm": Decimal("0.00"),
                "thigh_skinfold_mm": Decimal("27.00"),
                "tricep_skinfold_mm": Decimal("23.00"),
                "suprailiac_skinfold_mm": Decimal("20.00"),
                "humerus_diameter_cm": Decimal("6.70"),
                "femur_diameter_cm": Decimal("9.10"),
                "arm_circumference_cm": Decimal("31.00"),
                "thigh_circumference_cm": Decimal("58.10"),
                "pushups_reps": 10,
                "plank_seconds": 29,
                "cooper_distance_m": 1520,
                "observations": "Baixa tolerancia a estabilidade lombopelvica. [seed:test-data]",
            },
            {
                "assessed_at": date(2026, 2, 22),
                "age": 37,
                "weight_kg": Decimal("72.90"),
                "height_cm": Decimal("168.00"),
                "target_fat_percentage": Decimal("23.00"),
                "protocol": PhysicalAssessment.Protocol.CUSTOM,
                "waist_cm": Decimal("81.80"),
                "hip_cm": Decimal("100.00"),
                "chest_skinfold_mm": Decimal("0.00"),
                "abdomen_skinfold_mm": Decimal("0.00"),
                "thigh_skinfold_mm": Decimal("25.00"),
                "tricep_skinfold_mm": Decimal("20.00"),
                "suprailiac_skinfold_mm": Decimal("18.00"),
                "humerus_diameter_cm": Decimal("6.70"),
                "femur_diameter_cm": Decimal("9.10"),
                "arm_circumference_cm": Decimal("31.40"),
                "thigh_circumference_cm": Decimal("57.50"),
                "pushups_reps": 16,
                "plank_seconds": 52,
                "cooper_distance_m": 1710,
                "observations": "Melhora de controle motor e tolerancia ao treino. [seed:test-data]",
            },
        ],
        "postural": {
            "assessed_at": date(2026, 2, 22),
            "lateral_view": "Anteriorizacao de cabeca moderada e aumento de lordose lombar.",
            "anterior_view": "Rotacao interna de ombros, joelho direito com valgismo discreto.",
            "posterior_view": "Assimetria de escapulas e inclinacao pelvica leve para a direita.",
            "markings": "Priorizar respiracao, mobilidade toracica, gluteo medio e estabilidade central.",
            "observations": "Cenario de venda para programa de reabilitacao postural e dor lombar. [seed:test-data]",
            "photo_upload_ready": True,
        },
    },
}


def get_seed_profiles():
    return SEED_PROFILES


def get_seed_accounts(profile_key):
    profile = SEED_PROFILES[profile_key]
    return {
        "admin_username": profile["admin_username"],
        "staff_username": profile["staff_username"],
        "password": SEED_PASSWORD,
    }


def _seed_note(text):
    return f"{text} {SEED_NOTE}".strip()


@transaction.atomic
def populate_test_data(profile_key):
    profile = SEED_PROFILES[profile_key]
    tenant, _ = Tenant.objects.get_or_create(
        slug=profile["tenant_slug"],
        defaults={
            "name": profile["tenant_name"],
            "contact_name": profile["contact_name"],
            "contact_email": f"{profile_key}@seed.local",
            "contact_phone": "(11) 99999-0001",
            "plan": profile["plan"],
            "is_active": True,
            "notes": _seed_note(f"Tenant criada automaticamente para testes do perfil {profile['label']}.") ,
        },
    )
    if SEED_NOTE not in (tenant.notes or ""):
        tenant.notes = _seed_note((tenant.notes or "").strip())
        tenant.save(update_fields=["notes"])

    admin_user, _ = User.objects.get_or_create(
        username=profile["admin_username"],
        defaults={
            "full_name": f"{profile['label']} Admin",
            "email": f"{profile['admin_username']}@seed.local",
            "role": User.Role.TENANT_ADMIN,
            "is_staff": True,
            "is_active": True,
        },
    )
    admin_user.set_password(SEED_PASSWORD)
    admin_user.role = User.Role.TENANT_ADMIN
    admin_user.is_staff = True
    admin_user.is_active = True
    admin_user.save()

    staff_user, _ = User.objects.get_or_create(
        username=profile["staff_username"],
        defaults={
            "full_name": f"{profile['label']} Staff",
            "email": f"{profile['staff_username']}@seed.local",
            "role": User.Role.TENANT_STAFF,
            "is_staff": True,
            "is_active": True,
        },
    )
    staff_user.set_password(SEED_PASSWORD)
    staff_user.role = User.Role.TENANT_STAFF
    staff_user.is_staff = True
    staff_user.is_active = True
    staff_user.save()

    TenantMembership.objects.update_or_create(
        tenant=tenant,
        user=admin_user,
        defaults={"role": TenantMembership.Role.ADMIN, "is_default": True, "is_active": True},
    )
    TenantMembership.objects.update_or_create(
        tenant=tenant,
        user=staff_user,
        defaults={"role": TenantMembership.Role.STAFF, "is_default": False, "is_active": True},
    )
    tenant.primary_admin = admin_user
    tenant.save(update_fields=["primary_admin"])

    student_defaults = dict(profile["student"])
    student_defaults["notes"] = _seed_note(student_defaults["notes"])
    student, _ = Student.objects.update_or_create(
        tenant=tenant,
        full_name=profile["student"]["full_name"],
        birth_date=profile["student"]["birth_date"],
        defaults=student_defaults,
    )

    for payload in profile["physical"]:
        defaults = dict(payload)
        defaults["observations"] = _seed_note(defaults["observations"])
        PhysicalAssessment.objects.update_or_create(
            tenant=tenant,
            student=student,
            assessed_at=payload["assessed_at"],
            defaults=defaults,
        )

    postural_defaults = dict(profile["postural"])
    postural_defaults["observations"] = _seed_note(postural_defaults["observations"])
    PosturalAssessment.objects.update_or_create(
        tenant=tenant,
        student=student,
        assessed_at=profile["postural"]["assessed_at"],
        defaults=postural_defaults,
    )

    return {
        "tenant": tenant,
        "student": student,
        "assessment_count": PhysicalAssessment.objects.filter(tenant=tenant, student=student).count(),
        "profile_label": profile["label"],
        "accounts": get_seed_accounts(profile_key),
    }


@transaction.atomic
def delete_test_data(profile_key=None):
    profiles = {profile_key: SEED_PROFILES[profile_key]} if profile_key else SEED_PROFILES
    removed = {"tenants_deleted": 0, "users_deleted": 0}
    usernames = []
    slugs = [profile["tenant_slug"] for profile in profiles.values()] + LEGACY_SEED_SLUGS
    tenants = list(Tenant.objects.filter(slug__in=slugs))
    for tenant in tenants:
        usernames.extend(list(tenant.memberships.values_list("user__username", flat=True)))
        tenant.delete()
        removed["tenants_deleted"] += 1
    usernames.extend(LEGACY_SEED_USERNAMES)
    if usernames:
        removed["users_deleted"] = User.objects.filter(username__in=set(usernames)).delete()[0]
    return removed


def get_seed_status():
    statuses = []
    for key, profile in SEED_PROFILES.items():
        tenant = Tenant.objects.filter(slug=profile["tenant_slug"]).first()
        statuses.append(
            {
                "key": key,
                "label": profile["label"],
                "tenant": tenant,
                "admin_username": profile["admin_username"],
                "staff_username": profile["staff_username"],
                "password": SEED_PASSWORD,
                "student_name": profile["student"]["full_name"],
                "physical_target": len(profile["physical"]),
                "postural_target": 1,
                "student_count": tenant.students.count() if tenant else 0,
                "physical_count": tenant.physical_assessments.count() if tenant else 0,
                "postural_count": tenant.postural_assessments.count() if tenant else 0,
            }
        )
    return statuses

