from django.contrib import admin
from .models import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "url", "created_at")
    search_fields = ("name", "description", "tags")
    list_filter = ("status",)
