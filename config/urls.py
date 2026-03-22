from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import PublicLandingView, PublicPricingView

urlpatterns = [
    path("", PublicLandingView.as_view(), name="root"),
    path("planos/", PublicPricingView.as_view(), name="public_pricing"),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("tenant/", include("apps.core.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("admin-tools/", include("apps.tenants.urls")),
    path("alunos/", include("apps.students.urls")),
    path("avaliacoes/", include("apps.assessments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
