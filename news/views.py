from django.shortcuts import get_object_or_404, render

from .models import News


def news_list(request):
    return render(
        request,
        "news.html",
        {
            "news_items": News.objects.filter(is_published=True).prefetch_related("images"),
        },
    )


def news_detail(request, pk):
    news = get_object_or_404(
        News.objects.filter(is_published=True).prefetch_related("images"),
        pk=pk,
    )
    return render(request, "news_detail.html", {"news": news})
