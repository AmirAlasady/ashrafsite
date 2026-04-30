from django.shortcuts import get_object_or_404, render

from .models import AcademyItem


def academy_list(request):
    return render(
        request,
        "academy/list.html",
        {"items": AcademyItem.objects.prefetch_related("images").all()},
    )


def academy_detail(request, pk):
    item = get_object_or_404(AcademyItem.objects.prefetch_related("images"), pk=pk)
    return render(request, "academy/detail.html", {"item": item})
