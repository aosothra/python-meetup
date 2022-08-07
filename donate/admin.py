import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder

from donate.models import Donate
from import_export import resources
from import_export.admin import ExportMixin


class DonateResource(resources.ModelResource):
    class Meta:
        model = Donate


@admin.register(Donate)
class DonateAdmin(ExportMixin, admin.ModelAdmin):
    change_list_template = "admin/donate/donate/change_list.html"
    resource_class = DonateResource
    list_display = (
        "amount",
        "currency",
        "event",
        "telegram_id",
        "telegram_username",
        "created_at",
    )
    readonly_fields = (
        "telegram_username",
        "amount",
        "currency",
        "created_at",
    )

    def changelist_view(self, request, extra_context=None):
        chart = [
            {
                # "x": d.telegram_username if d.telegram_username else "Anonimus",
                "created_at": d.created_at,
                "y": d.amount,
            }
            for d in Donate.objects.all()
        ]
        serialized_chart = json.dumps(chart, cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": serialized_chart}
        return super().changelist_view(request, extra_context=extra_context)
