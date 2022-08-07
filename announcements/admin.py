from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from announcements.models import Announcement

# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    ordering = ("released_on",)
    list_display = (
        "id",
        "created_on",
        "event",
        "message",
        "released_on",
        "announce_button",
    )

    @admin.display(description="Действия")
    def announce_button(self, obj):
        if not obj.released_on:
            return mark_safe(
                render_to_string("announce_button.html", context={"id": obj.id})
            )
        else:
            return None
