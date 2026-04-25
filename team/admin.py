from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order")
    list_editable = ("role", "order")
    search_fields = ("name", "role")
