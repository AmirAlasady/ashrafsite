from django.shortcuts import render

from .models import News


def news_list(request):
    return render(
        request,
        "news.html",
        {
            "news_items": News.objects.filter(is_published=True).prefetch_related("images"),
        },
    )
