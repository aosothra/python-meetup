from django.db import models

class Donate(models.Model):
    """Donate model"""

    telegram_username = models.CharField(
        "Логин в телеграмме",
        max_length=32,
        null=True,
        blank=True,
    )

    amount = models.IntegerField(
        'Сумма'
    )

    currency = models.CharField(
        'Валюта',
        max_length = 3,
        default = 'RUB'
    )

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

    def __str__(self):
        return f"{self.telegram_username}, {self.amount} {self.currency}"