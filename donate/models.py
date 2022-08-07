from convention.models import Event
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Donate(models.Model):
    """Donate model"""

    telegram_id = models.IntegerField("ID в телеграмме")
    telegram_username = models.CharField(
        "Логин в телеграмме",
        max_length=32,
        null=True,
        blank=True,
    )

    amount = models.IntegerField(
        "Сумма",
        validators=[
            MinValueValidator(65),
            MaxValueValidator(1000),
        ],
    )

    currency = models.CharField(
        "Валюта",
        max_length=3,
        default="RUB",
    )

    created_at = models.DateTimeField(
        "Дата транзакции",
        default=timezone.now,
    )

    event = models.ForeignKey(
        Event,
        related_name="donations",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

    def __str__(self):
        return f"{self.telegram_username}, {self.amount} {self.currency}"
