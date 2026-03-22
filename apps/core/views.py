from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.accounts.models import User
from apps.tenants.models import Tenant, TenantMembership

from .forms import PublicLeadForm


def _normalize_whatsapp(phone):
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    return digits


def _get_public_sales_contact():
    return (
        User.objects.filter(
            is_active=True,
            is_public_sales_contact=True,
            whatsapp_phone__gt="",
            tenant_memberships__role=TenantMembership.Role.ADMIN,
            tenant_memberships__is_active=True,
            tenant_memberships__tenant__is_active=True,
        )
        .distinct()
        .order_by("full_name", "username")
        .first()
    )


def _build_sales_contact_context():
    contact = _get_public_sales_contact()
    if not contact:
        return {"sales_contact": None, "sales_whatsapp_url": "", "sales_whatsapp_label": ""}

    digits = _normalize_whatsapp(contact.whatsapp_phone)
    if not digits:
        return {"sales_contact": None, "sales_whatsapp_url": "", "sales_whatsapp_label": ""}

    label = contact.full_name or contact.username
    message = quote(f"Ola {label}, vi o site demo do SaaS Davi Alves Personal e quero falar sobre os planos.")
    return {
        "sales_contact": contact,
        "sales_whatsapp_label": label,
        "sales_whatsapp_url": f"https://wa.me/{digits}?text={message}",
    }


class PublicLandingView(TemplateView):
    template_name = "core/public_landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "feature_cards": [
                    {
                        "title": "Cockpit de Performance",
                        "description": "Dashboard com leitura rapida de alunos, avaliacoes e indicadores de composicao corporal.",
                        "icon": "bi-speedometer2",
                    },
                    {
                        "title": "Avaliacao Profissional",
                        "description": "Fluxo de avaliacao fisica e postural pronto para rotina comercial de personal, estudio e equipe.",
                        "icon": "bi-clipboard2-pulse",
                    },
                    {
                        "title": "SaaS Multi-tenant",
                        "description": "Base pronta para vender acesso por tenant, com separacao segura de dados e visao master global.",
                        "icon": "bi-diagram-3",
                    },
                ],
                "showcase_metrics": [
                    {"label": "Tempo de onboarding", "value": "1 dia", "helper": "base pronta para operar"},
                    {"label": "Perfis iniciais", "value": "4", "helper": "seeds comerciais e tecnicos"},
                    {"label": "Operacao", "value": "360", "helper": "visao aluno + avaliacao + tenant"},
                ],
                "journey_steps": [
                    "Explore o demo e avalie a experiencia visual e operacional.",
                    "Escolha o plano ideal para seu volume de alunos e equipe.",
                    "Com o pagamento confirmado, sua tenant e seu acesso entram em operacao.",
                ],
            }
        )
        context.update(_build_sales_contact_context())
        return context


class PublicPricingView(TemplateView):
    template_name = "core/public_pricing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PublicLeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            messages.success(request, f"Recebemos seu interesse no plano {lead.get_plan_interest_display() if hasattr(lead, 'get_plan_interest_display') else lead.plan_interest.title()}. Nossa equipe comercial pode seguir por WhatsApp ou e-mail.")
            return redirect("public_pricing")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plans"] = [
            {
                "name": "Start",
                "price": "R$ 97",
                "period": "/mes",
                "description": "Para personal individual iniciando a operacao digital.",
                "features": ["1 tenant", "ate 60 alunos", "avaliacao fisica e postural", "dashboard operacional"],
                "highlight": False,
            },
            {
                "name": "Pro",
                "price": "R$ 197",
                "period": "/mes",
                "description": "Para personal com base ativa e foco em conversao premium.",
                "features": ["1 tenant", "ate 200 alunos", "equipe interna da tenant", "relatorios e seeds de demonstracao"],
                "highlight": True,
            },
            {
                "name": "Team",
                "price": "R$ 397",
                "period": "/mes",
                "description": "Para estudio ou pequena equipe com operacao compartilhada.",
                "features": ["1 tenant com multiplos usuarios", "alunos ilimitados", "visao de equipe", "base pronta para escalar"],
                "highlight": False,
            },
        ]
        context["comparison_rows"] = [
            ("Limite de alunos", "ate 60", "ate 200", "ilimitado"),
            ("Usuarios da tenant", "1 admin", "1 admin + staff", "equipe completa"),
            ("Avaliacao fisica", "sim", "sim", "sim"),
            ("Avaliacao postural", "sim", "sim", "sim"),
            ("Seeds de demonstracao", "nao", "sim", "sim"),
            ("Estrutura para escala", "base", "avancada", "prioritaria"),
        ]
        context["faq_items"] = [
            {
                "question": "Depois de pagar eu recebo acesso imediato?",
                "answer": "A proposta atual considera confirmacao comercial e liberacao da tenant pelo gestor SaaS. Na proxima etapa isso pode virar provisionamento automatico.",
            },
            {
                "question": "Posso come?ar com poucos alunos e crescer depois?",
                "answer": "Sim. A estrutura de planos foi pensada para upgrade progressivo sem retrabalho operacional.",
            },
            {
                "question": "O sistema ja esta preparado para multi-tenant?",
                "answer": "Sim. Toda a base ja nasce com tenant ativa por sessao, separacao logica dos dados e visao master global.",
            },
            {
                "question": "Existe suporte para estudios ou pequenas equipes?",
                "answer": "Sim. O plano Team cobre operacao compartilhada com usuarios por tenant e visao de gestao mais completa.",
            },
        ]
        context["lead_form"] = kwargs.get("form") or PublicLeadForm()
        context.update(_build_sales_contact_context())
        return context


@login_required
def switch_tenant(request):
    if request.method != "POST":
        return redirect("dashboard:home")

    tenant_id = (request.POST.get("tenant_id") or "").strip()
    next_url = request.POST.get("next") or "dashboard:home"

    if request.user.is_superuser:
        if not tenant_id:
            request.session.pop(settings.TENANT_SESSION_KEY, None)
            messages.info(request, "Visualizacao da tenant encerrada.")
            return redirect(request.POST.get("next") or "dashboard:control_center")

        tenant = Tenant.objects.filter(pk=tenant_id).first()
        if tenant:
            request.session[settings.TENANT_SESSION_KEY] = tenant.id
            messages.success(request, f"Tenant ativa alterada para {tenant.name}.")
        else:
            request.session.pop(settings.TENANT_SESSION_KEY, None)
            messages.error(request, "Tenant informada nao foi encontrada.")
        return redirect(next_url)

    if not tenant_id:
        messages.error(request, "Selecione uma tenant valida.")
        return redirect(next_url)

    membership = TenantMembership.objects.filter(
        user=request.user,
        tenant_id=tenant_id,
        is_active=True,
        tenant__is_active=True,
    ).first()
    if membership:
        request.session[settings.TENANT_SESSION_KEY] = membership.tenant_id
        messages.success(request, f"Tenant ativa alterada para {membership.tenant.name}.")
    else:
        messages.error(request, "Voce nao possui acesso a essa tenant.")
    return redirect(next_url)
