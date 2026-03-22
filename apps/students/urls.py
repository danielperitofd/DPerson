from django.urls import path

from .views import StudentCreateView, StudentDeleteView, StudentDetailView, StudentListView, StudentUpdateView

app_name = "students"

urlpatterns = [
    path("", StudentListView.as_view(), name="list"),
    path("novo/", StudentCreateView.as_view(), name="create"),
    path("<int:pk>/", StudentDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", StudentUpdateView.as_view(), name="update"),
    path("<int:pk>/excluir/", StudentDeleteView.as_view(), name="delete"),
]
