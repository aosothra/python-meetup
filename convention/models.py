from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Attendee(models.Model):
    """Event attendee model"""

    telegram_id = models.IntegerField("ID в телеграмме", primary_key=True)
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


class Event(models.Model):
    title = models.CharField(
        "Название ивента",
        max_length=32,
    )

    class Meta:
        verbose_name = "Ивент"
        verbose_name_plural = "Ивенты"

    def __str__(self):
        return self.title


class Flow(models.Model):
    title = models.CharField(
        "Название потока",
        max_length=32,
    )
    event = models.ForeignKey(
        Event,
        related_name="flows",
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
        max_length=32,
    )
    flow = models.ForeignKey(
        Flow,
        related_name="blocks",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Блок докладов"
        verbose_name_plural = "Блоки докладов"

    def __str__(self):
        return f"{self.flow.event.title} / {self.flow.title} / {self.title}"


class Presentation(models.Model):
    title = models.CharField(
        "Название выступления",
        max_length=32,
    )
    block = models.ForeignKey(
        Block,
        related_name="presentations",
        on_delete=models.CASCADE,
    )
    speaker = models.ForeignKey(
        Attendee,
        related_name="presentations",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Выступление"
        verbose_name_plural = "Выступления"

    def __str__(self):
        return f"{self.block.flow.event.title} / {self.title} - {self.speaker}"
