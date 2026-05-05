from django.contrib import admin

from .models import (
    AboutInfo,
    Banner,
    BehindTheScenesImage,
    BestWork,
    BTSGalleryImage,
    CastingPage,
    CastingSlide,
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


@admin.register(BestWork)
class BestWorkAdmin(admin.ModelAdmin):
    list_display = ("__str__", "caption", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("caption",)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "label", "is_active", "order", "created_at")
    list_editable = ("is_active", "order")
    search_fields = ("title", "label")
    fieldsets = (
        (None, {
            "fields": ("title", "description", "label"),
        }),
        ("Media (use one, not both)", {
            "fields": ("image", "video"),
        }),
        ("Optional button", {
            "fields": ("button_label", "button_url"),
        }),
        ("Production details", {
            "fields": ("production_type", "production_year", "production_quality"),
            "description": "Shown next to the button: Type · Year · Quality.",
        }),
        ("Display", {
            "fields": ("is_active", "order"),
        }),
    )


@admin.register(CastingPage)
class CastingPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "headline", "updated_at")


@admin.register(CastingSlide)
class CastingSlideAdmin(admin.ModelAdmin):
    list_display = ("__str__", "headline", "order")
    list_editable = ("order",)
    ordering = ("order",)
