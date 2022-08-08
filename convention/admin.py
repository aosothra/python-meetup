from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin

from convention.models import Attendee, Block, Event, Flow, Presentation


class PresentationInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Presentation
    show_change_link = True
    extra = 0
    fields = (
        "order_number",
        "title",
    )
    sortable_field_name = "order_number"


class BlockInline(admin.TabularInline):
    model = Block
    fields = ("title", "moderator", "starts_at", "ends_at")
    show_change_link = True
    extra = 0


class FlowInline(admin.TabularInline):
    model = Flow
    show_change_link = True
    extra = 0


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
    inlines = [
        FlowInline,
    ]


@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display = (
        "event",
        "title",
    )
    search_fields = (
        "event__title",
        "title",
    )
    inlines = [
        BlockInline,
    ]


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "flow",
        "title",
        "get_moderator_name",
        "starts_at",
        "ends_at",
        "presentation_count",
    )
    list_filter = ("flow",)
    search_fields = (
        "title",
        "moderator__firstname",
        "moderator__lastname",
    )
    inlines = [
        PresentationInline,
    ]

    @admin.display(description="Всего докладов", empty_value="-")
    def presentation_count(sefl, obj):
        count = obj.presentations.count()
        if count:
            return count

    @admin.display(description="Модератор")
    def get_moderator_name(sefl, obj):
        if obj.moderator:
            return f"{obj.moderator.firstname} {obj.moderator.lastname}"


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = (
        "block",
        "title",
    )
    readonly_fields = ("order_number",)
    search_fields = ("title",)
