from django.contrib import admin
from .models import CaseStudy, Service, TeamMember, Testimonial

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "is_featured", "display_order", "updated_at")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("display_order", "title")

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "project_date", "created_at")
    list_filter = ("service", "project_date")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "project_date"
    autocomplete_fields = ("service",)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "company", "is_featured", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("client_name", "company", "quote")

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "bio")
    ordering = ("display_order", "name")
