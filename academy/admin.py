from django.contrib import admin

from .models import AcademyItem, AcademyItemImage


class AcademyItemImageInline(admin.TabularInline):
    model = AcademyItemImage
    extra = 1


@admin.register(AcademyItem)
class AcademyItemAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("name", "bio")
    inlines = [AcademyItemImageInline]


@admin.register(AcademyItemImage)
class AcademyItemImageAdmin(admin.ModelAdmin):
    list_display = ("item", "order", "caption")
    list_editable = ("order",)
