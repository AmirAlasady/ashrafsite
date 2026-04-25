from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "sent_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "sent_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("sent_at",)
