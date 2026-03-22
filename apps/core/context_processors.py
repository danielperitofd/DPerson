from apps.core.permissions import TenantPermissions, user_has_tenant_permission
from apps.tenants.models import Tenant, TenantMembership


def shell_context(request):
    active_tenant = getattr(request, "active_tenant", None)
    memberships = []
    all_tenants = []
    can_manage_users = False
    is_master_preview = False
    if request.user.is_authenticated:
        memberships = TenantMembership.objects.filter(user=request.user, is_active=True).select_related("tenant")
        if request.user.is_superuser:
            all_tenants = Tenant.objects.all().order_by("name")
            is_master_preview = active_tenant is not None
        can_manage_users = user_has_tenant_permission(request.user, active_tenant, TenantPermissions.USERS)
    return {
        "active_tenant": active_tenant,
        "tenant_memberships": memberships,
        "all_tenants": all_tenants,
        "can_manage_users": can_manage_users,
        "is_master_preview": is_master_preview,
    }
