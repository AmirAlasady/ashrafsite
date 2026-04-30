from django.shortcuts import render

from team.models import Member

from .models import (
    AboutInfo,
    BTSGalleryImage,
    BehindTheScenesImage,
    BestWork,
    CastingPage,
    CastingSlide,
    Client,
    HeroDescription,
    HeroSection,
    Post,
)


def home(request):
    # Singleton-style: return whatever row exists; only create one if the
    # table is completely empty. This avoids creating a new pk=1 row that
    # silently shadows admin edits made on a different pk.
    hero_description = HeroDescription.objects.first()
    if hero_description is None:
        hero_description = HeroDescription.objects.create()

    context = {
        "hero": HeroSection.objects.filter(is_active=True).first(),
        "hero_description": hero_description,
        "clients": Client.objects.all(),
        "best_works": BestWork.objects.all(),
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


def bts_gallery(request):
    return render(
        request,
        "behind_the_scenes.html",
        {"images": BTSGalleryImage.objects.all()},
    )


def casting(request):
    casting_obj = CastingPage.objects.first()
    if casting_obj is None:
        casting_obj = CastingPage.objects.create()

    slides = list(CastingSlide.objects.all())
    if not slides:
        # Fall back to the CastingPage's own content as a single slide so the
        # template only needs to know about a uniform `slides` list.
        slides = [casting_obj]

    return render(
        request,
        "casting.html",
        {"casting": casting_obj, "slides": slides},
    )
