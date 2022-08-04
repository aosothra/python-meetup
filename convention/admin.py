from django.contrib import admin

from convention.models import Attendee, Block, Event, Flow, Presentation


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    pass


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    pass
