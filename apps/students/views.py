from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.core.mixins import TenantObjectPermissionMixin, TenantPermissionRequiredMixin
from apps.core.permissions import TenantPermissions

from .forms import StudentForm
from .models import Student


class StudentListView(TenantPermissionRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    paginate_by = 12
    required_tenant_permission = TenantPermissions.STUDENTS

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)
            )
        status = self.request.GET.get("status")
        if status in {"active", "inactive"}:
            queryset = queryset.filter(is_active=(status == "active"))
        return queryset


class StudentDetailView(TenantObjectPermissionMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"
    required_tenant_permission = TenantPermissions.STUDENTS


class StudentCreateView(TenantPermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:list")
    required_tenant_permission = TenantPermissions.STUDENTS

    def form_valid(self, form):
        messages.success(self.request, "Aluno cadastrado com sucesso.")
        return super().form_valid(form)


class StudentUpdateView(TenantObjectPermissionMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:list")
    required_tenant_permission = TenantPermissions.STUDENTS

    def form_valid(self, form):
        messages.success(self.request, "Aluno atualizado com sucesso.")
        return super().form_valid(form)


class StudentDeleteView(TenantObjectPermissionMixin, DeleteView):
    model = Student
    template_name = "shared/confirm_delete.html"
    success_url = reverse_lazy("students:list")
    required_tenant_permission = TenantPermissions.STUDENTS

    def form_valid(self, form):
        messages.success(self.request, "Aluno excluido com sucesso.")
        return super().form_valid(form)
