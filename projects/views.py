from django.shortcuts import get_object_or_404, render

from .models import Project


def project_list(request):
    return render(
        request,
        "projects/list.html",
        {"projects": Project.objects.prefetch_related("images").all()},
    )


def project_detail(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related("images"), pk=pk)
    return render(request, "projects/detail.html", {"project": project})
