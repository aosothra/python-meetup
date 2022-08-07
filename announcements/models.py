from django.db import models
from django.utils import timezone

from convention.models import Event


class Announcement(models.Model):
    message = models.TextField("Сообщение")
    event = models.ForeignKey(
        Event,
        related_name="anouncements",
        verbose_name="Мероприятие",
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(
        "Время создания", default=timezone.now, editable=False
    )
    released_on = models.DateTimeField(
        "Время рассылки оповещения", null=True, editable=False
    )

    class Meta:
        verbose_name = "Оповещение"
        verbose_name_plural = "Оповещения"

    def __str__(self):
        return f"{self.created_on}: {self.message}"
