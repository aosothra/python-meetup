import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder

from donate.models import Donate


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    readonly_fields = ["telegram_username", "amount", "currency"]

    def changelist_view(self, request, extra_context=None):
        chart = [
            {
                "x": d.telegram_username if d.telegram_username else "Anonimus",
                "y": d.amount,
            }
            for d in Donate.objects.all()
        ]
        serialized_chart = json.dumps(chart, cls=DjangoJSONEncoder)
        print()
        print(serialized_chart)
        print()
        extra_context = extra_context or {"chart_data": serialized_chart}
        return super().changelist_view(request, extra_context=extra_context)
