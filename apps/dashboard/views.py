import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assessments.models import PhysicalAssessment, PosturalAssessment
from apps.students.models import Student
from apps.tenants.models import Tenant


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.request.active_tenant
        if self.request.user.is_superuser and tenant is None:
            context.update(
                {
                    "mode": "master",
                    "tenant_count": Tenant.objects.count(),
                    "active_tenant_count": Tenant.objects.filter(is_active=True).count(),
                    "student_count": Student.objects.count(),
                    "insights": [
                        "Ative uma tenant no seletor superior para visualizar metricas operacionais detalhadas.",
                        "A arquitetura ja esta preparada para evolucao com PostgreSQL e permissoes por perfil.",
                    ],
                    "chart_labels": json.dumps([]),
                    "chart_values": json.dumps([]),
                }
            )
            return context

        students = Student.objects.filter(tenant=tenant)
        physical = PhysicalAssessment.objects.filter(tenant=tenant)
        postural = PosturalAssessment.objects.filter(tenant=tenant)
        latest_physical = physical.first()
        evolution = []
        for assessment in physical.order_by("assessed_at")[:6]:
            evolution.append({"label": assessment.assessed_at.strftime("%d/%m"), "value": float(assessment.body_fat_percentage or 0)})
        context.update(
            {
                "mode": "tenant",
                "student_count": students.count(),
                "active_student_count": students.filter(is_active=True).count(),
                "physical_count": physical.count(),
                "postural_count": postural.count(),
                "avg_bmi": physical.aggregate(value=Avg("bmi"))["value"] or 0,
                "avg_body_fat": physical.aggregate(value=Avg("body_fat_percentage"))["value"] or 0,
                "recent_students": students.order_by("-created_at")[:5],
                "latest_assessment": latest_physical,
                "insights": self.build_insights(students.count(), physical.count(), latest_physical),
                "chart_labels": json.dumps([item["label"] for item in evolution]),
                "chart_values": json.dumps([item["value"] for item in evolution]),
            }
        )
        return context

    @staticmethod
    def build_insights(student_count, assessment_count, latest_assessment):
        insights = []
        if student_count < 10:
            insights.append("Sua operacao esta leve. Esse e um bom momento para padronizar protocolos e acelerar captacao.")
        else:
            insights.append("Sua base de alunos ja comporta automacoes de reavaliacao e esteira comercial.")
        if assessment_count == 0:
            insights.append("Nenhuma avaliacao fisica cadastrada ainda. O dashboard destrava melhor quando ha historico.")
        elif latest_assessment and latest_assessment.body_fat_percentage > 25:
            insights.append("Ultima avaliacao com gordura elevada. Vale destacar plano de reducao e checkpoints quinzenais.")
        else:
            insights.append("Os indicadores recentes estao em linha. Aproveite para construir relatorios comparativos.")
        return insights


class MasterControlCenterView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/master_control_center.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenants = Tenant.objects.annotate(
            total_students=Count("students", distinct=True),
            total_physical=Count("physical_assessments", distinct=True),
            total_postural=Count("postural_assessments", distinct=True),
        ).order_by("-created_at", "name")[:8]
        physical = PhysicalAssessment.objects.all()
        context.update(
            {
                "tenant_count": Tenant.objects.count(),
                "active_tenant_count": Tenant.objects.filter(is_active=True).count(),
                "inactive_tenant_count": Tenant.objects.filter(is_active=False).count(),
                "student_count": Student.objects.count(),
                "physical_count": physical.count(),
                "postural_count": PosturalAssessment.objects.count(),
                "avg_bmi": physical.aggregate(value=Avg("bmi"))["value"] or 0,
                "avg_body_fat": physical.aggregate(value=Avg("body_fat_percentage"))["value"] or 0,
                "tenants": tenants,
                "selected_preview_tenant": self.request.active_tenant,
            }
        )
        return context
