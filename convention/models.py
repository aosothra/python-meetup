from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Attendee(models.Model):
    """Event attendee model"""

    telegram_id = models.IntegerField("ID в телеграмме", primary_key=True)
    firstname = models.CharField(
        "Имя",
        max_length=40,
        null=True,
        blank=True,
    )
    lastname = models.CharField(
        "Фамилия",
        max_length=40,
        null=True,
        blank=True,
    )
    company = models.CharField(
        "Место работы",
        max_length=100,
        null=True,
        blank=True,
    )
    position = models.CharField(
        "Должность",
        max_length=100,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def is_anonymous(self):
        return not all([self.firstname, self.lastname, self.company, self.position])

    def is_speaker(self):
        try:
            self.speeches
            return True
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return self.telegram_id
