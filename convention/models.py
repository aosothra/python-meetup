from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Event(models.Model):
    title = models.CharField(
        "Название ивента",
        max_length=32,
    )
    starting_date = models.DateField("День начала ивента")
    ending_date = models.DateField("День окончания ивента")

    class Meta:
        verbose_name = "Ивент"
        verbose_name_plural = "Ивенты"

    def __str__(self):
        return self.title


class Attendee(models.Model):
    """Event attendee model"""

    id = models.AutoField("ID", primary_key=True)
    telegram_id = models.IntegerField("ID в телеграмме")
    event = models.ForeignKey(
        Event, related_name="attendees", verbose_name="Ивент", on_delete=models.CASCADE
    )
    telegram_username = models.CharField(
        "Логин в телеграмме",
        max_length=32,
        null=True,
        blank=True,
    )
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
        unique_together = ("telegram_id", "event")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    def get_networking_application(self):
        return f"{self.firstname} {self.lastname}\n{self.position}\n{self.company}"

    def is_anonymous(self):
        return not all(
            [
                self.telegram_username,
                self.firstname,
                self.lastname,
                self.company,
                self.position,
            ]
        )

    def is_speaker(self):
        try:
            self.speeches
            return True
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        name = (
            f"{self.firstname} {self.lastname}"
            if not self.is_anonymous()
            else "Анонимный участник"
        )
        return f"{self.telegram_id} - {name}"


class Flow(models.Model):
    title = models.CharField(
        "Название потока",
        max_length=32,
    )
    event = models.ForeignKey(
        Event,
        related_name="flows",
        verbose_name="Ивент",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"

    def __str__(self):
        return f"{self.event.title} / {self.title}"


class Block(models.Model):
    title = models.CharField(
        "Название блока",
        max_length=100,
    )
    description = models.TextField("Описание блока", null=True, blank=True)
    moderator = models.ForeignKey(
        Attendee,
        related_name="moderated_blocks",
        verbose_name="Модератор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    flow = models.ForeignKey(
        Flow,
        related_name="blocks",
        verbose_name="Поток",
        on_delete=models.CASCADE,
    )
    starts_at = models.DateTimeField("Время начала блока")
    ends_at = models.DateTimeField("Время окончания блока")

    class Meta:
        verbose_name = "Блок докладов"
        verbose_name_plural = "Блоки докладов"

    def __str__(self):
        return f"{self.flow.event.title} / {self.flow.title} / {self.title}"


class Presentation(models.Model):
    title = models.CharField(
        "Название выступления",
        max_length=100,
    )
    block = models.ForeignKey(
        Block,
        related_name="presentations",
        verbose_name="Блок",
        on_delete=models.CASCADE,
    )
    speakers = models.ManyToManyField(
        Attendee,
        related_name="presentations",
        verbose_name="Спикеры",
    )

    class Meta:
        verbose_name = "Выступление"
        verbose_name_plural = "Выступления"

    def __str__(self):
        return f"{self.block.flow.event.title} / {self.title} - {self.speaker}"
