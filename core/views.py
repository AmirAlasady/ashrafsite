from django.shortcuts import render

from team.models import Member

from .models import (
    AboutInfo,
    BehindTheScenesImage,
    Client,
    HeroDescription,
    HeroSection,
    Post,
)


def home(request):
    hero_description, _ = HeroDescription.objects.get_or_create(pk=1)
    context = {
        "hero": HeroSection.objects.filter(is_active=True).first(),
        "hero_description": hero_description,
        "clients": Client.objects.all(),
        "bts_images": BehindTheScenesImage.objects.all(),
        "posts": Post.objects.filter(is_published=True)[:6],
    }
    return render(request, "home.html", context)


def about(request):
    context = {
        "about_info": AboutInfo.objects.first(),
        "members": Member.objects.all(),
    }
    return render(request, "about.html", context)
