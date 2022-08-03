from django.contrib import admin

from convention.models import Attendee


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    pass
