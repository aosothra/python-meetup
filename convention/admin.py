from django.contrib import admin

from convention.models import Attendee, Block, Event, Flow, Presentation


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = (
        "firstname",
        "lastname",
        "telegram_id",
        "telegram_username",
        "company",
        "position",
    )
    readonly_fields = (
        "telegram_id",
        "telegram_username",
    )
    search_fields = (
        "firstname",
        "lastname",
        "telegram_id",
        "telegram_username",
        "company",
        "position",
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "starting_date",
        "ending_date",
    )
    list_filter = (
        "starting_date",
        "ending_date",
    )
    search_fields = ("title",)


@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "title",
    )
    search_fields = (
        "event",
        "title",
    )


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "flow",
        "title",
        "moderator",
        "starts_at",
        "ends_at",
    )
    search_fields = (
        "title",
        "moderator",
    )


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = (
        "block",
        "title",
    )
    search_fields = ("title",)
