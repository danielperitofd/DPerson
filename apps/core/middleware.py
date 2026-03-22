from django.conf import settings

from apps.tenants.models import Tenant, TenantMembership


class ActiveTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.active_tenant = None
        if request.user.is_authenticated:
            active_tenant_id = request.session.get(settings.TENANT_SESSION_KEY)
            if request.user.is_superuser and active_tenant_id:
                request.active_tenant = Tenant.objects.filter(pk=active_tenant_id).first()
            else:
                memberships = TenantMembership.objects.filter(
                    user=request.user,
                    is_active=True,
                    tenant__is_active=True,
                ).select_related("tenant")
                membership = None
                if active_tenant_id:
                    membership = memberships.filter(tenant_id=active_tenant_id).first()
                if membership is None:
                    membership = memberships.order_by("-is_default", "tenant__name").first()
                if membership:
                    request.active_tenant = membership.tenant
                    request.session[settings.TENANT_SESSION_KEY] = membership.tenant_id
        return self.get_response(request)
