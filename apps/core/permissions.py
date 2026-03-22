from apps.tenants.models import TenantMembership


class TenantPermissions:
    DASHBOARD = "dashboard.view"
    STUDENTS = "students.manage"
    ASSESSMENTS = "assessments.manage"
    REPORTS = "reports.view"
    USERS = "users.manage"
    TENANTS = "tenants.manage"


ROLE_PERMISSION_MAP = {
    TenantMembership.Role.ADMIN: {
        TenantPermissions.DASHBOARD,
        TenantPermissions.STUDENTS,
        TenantPermissions.ASSESSMENTS,
        TenantPermissions.REPORTS,
        TenantPermissions.USERS,
    },
    TenantMembership.Role.STAFF: {
        TenantPermissions.DASHBOARD,
        TenantPermissions.STUDENTS,
        TenantPermissions.ASSESSMENTS,
        TenantPermissions.REPORTS,
    },
}


def get_membership(user, tenant):
    if not user.is_authenticated or tenant is None:
        return None
    return TenantMembership.objects.filter(user=user, tenant=tenant, is_active=True, tenant__is_active=True).first()


def user_has_tenant_permission(user, tenant, permission):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    membership = get_membership(user, tenant)
    if membership is None:
        return False
    return permission in ROLE_PERMISSION_MAP.get(membership.role, set())
