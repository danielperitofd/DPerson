from django.urls import path

from .views import (
    PhysicalAssessmentCreateView,
    PhysicalAssessmentDeleteView,
    PhysicalAssessmentListView,
    PhysicalAssessmentUpdateView,
    PosturalAssessmentCreateView,
    PosturalAssessmentDeleteView,
    PosturalAssessmentListView,
    PosturalAssessmentUpdateView,
)

app_name = "assessments"

urlpatterns = [
    path("fisicas/", PhysicalAssessmentListView.as_view(), name="physical_list"),
    path("fisicas/nova/", PhysicalAssessmentCreateView.as_view(), name="physical_create"),
    path("fisicas/<int:pk>/editar/", PhysicalAssessmentUpdateView.as_view(), name="physical_update"),
    path("fisicas/<int:pk>/excluir/", PhysicalAssessmentDeleteView.as_view(), name="physical_delete"),
    path("posturais/", PosturalAssessmentListView.as_view(), name="postural_list"),
    path("posturais/nova/", PosturalAssessmentCreateView.as_view(), name="postural_create"),
    path("posturais/<int:pk>/editar/", PosturalAssessmentUpdateView.as_view(), name="postural_update"),
    path("posturais/<int:pk>/excluir/", PosturalAssessmentDeleteView.as_view(), name="postural_delete"),
]
