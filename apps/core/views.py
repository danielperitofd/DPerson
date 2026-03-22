from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.tenants.models import Tenant, TenantMembership


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
