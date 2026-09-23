from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "phone", "project_type", "status")
    list_filter = ("status", "project_type", "created_at")
    search_fields = ("name", "email", "phone", "message")
    date_hierarchy = "created_at"
    list_editable = ("status",)
    readonly_fields = ("name", "email", "phone", "project_type", "message", "attachment", "created_at")
    fields = ("status", "name", "email", "phone", "project_type", "message", "attachment", "created_at")
    ordering = ("-created_at",)
    list_per_page = 30
