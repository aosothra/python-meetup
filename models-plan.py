from tkinter import CASCADE
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    def is_speaker(self):
        """Участник выступает"""

        try:
            self.speeches
            return True
        except Speech.DoesNotExist:
            return False

    def __str__(self):
        return self.telegram_id


class Event(models.Model):
    """Поток мероприятия"""

    title = models.CharField(
        "Название потока",
        max_length=100,
    )

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"

    def __str__(self):
        return self.title


class EventBlock(models.Model):
    """Блок выступлений"""

    title = models.CharField(
        "Название блока",
        max_length=100,
    )

    event = models.ForeignKey(
        Event, verbose_name="Поток", related_name="blocks", on_delete=models.CASCADE
    )

    starts_on = models.DateTimeField(
        "Время начала блока",
    )

    ends_on = models.DateTimeField(
        "Время окончания блока",
    )

    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блоки"

    def __str__(self):
        return self.title


class Speech(models.Model):
    """Выступление"""

    title = models.CharField(
        "Название блока",
        max_length=100,
    )
    speakers = models.ManyToManyField(
        Attendee,
        related_name="speeches",
        verbose_name="Спикеры",
    )
    block = models.ForeignKey(
        EventBlock,
        related_name="speeches",
        verbose_name="Блок",
        on_delete=models.CASCADE,
    )
    starts_on = models.DateTimeField(
        "Время начала выступления",
    )
    ends_on = models.DateTimeField(
        "Время окончания выступления",
    )

    class Meta:
        verbose_name = "Выступление"
        verbose_name_plural = "Выступления"

    def __str__(self):
        return self.title


class Question(models.Model):
    """Вопрос к выступающему"""

    asker = models.ForeignKey(
        Attendee,
        related_name="asked_questions",
        verbose_name="Автор вопроса",
        on_delete=models.CASCADE,
    )
    question_text = models.TextField("Содержание вопроса")
    asked_on = models.DateTimeField("Время поступления вопроса")
    reciever = models.ForeignKey(
        Attendee,
        related_name="recieved_questions",
        verbose_name="Опрашиваемый спикер",
        on_delete=models.CASCADE,
    )
    answer_text = models.TextField(
        "Содержание ответа",
        null=True,
        blank=True,
    )
    answered_on = models.DateTimeField(
        "Время поступления ответа",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.asker} - {self.reciever}"
