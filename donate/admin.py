from django.contrib import admin

from donate.models import Donate

@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    readonly_fields = ['telegram_username', 'amount', 'currency']
