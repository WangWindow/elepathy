from django.contrib import admin
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "email", "order"]
    search_fields = ["name", "role"]
    list_editable = ["order"]
