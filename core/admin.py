from django.contrib import admin

from .models import (
    AboutInfo,
    BehindTheScenesImage,
    BTSGalleryImage,
    CastingPage,
    Client,
    FooterInfo,
    HeroDescription,
    HeroSection,
    Post,
)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    list_editable = ("is_active",)


@admin.register(HeroDescription)
class HeroDescriptionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "website")
    list_editable = ("order",)


@admin.register(BehindTheScenesImage)
class BehindTheScenesImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "animation", "order")
    list_editable = ("animation", "order")


@admin.register(FooterInfo)
class FooterInfoAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "phone")


@admin.register(AboutInfo)
class AboutInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name", "description")


@admin.register(BTSGalleryImage)
class BTSGalleryImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "created_at")
    list_editable = ("order",)


@admin.register(CastingPage)
class CastingPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
