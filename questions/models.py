from django.db import models

from convention.models import Attendee

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(
        Attendee,
        related_name="asked_questions",
        verbose_name="Автор вопроса",
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        Attendee,
        related_name="answered_questions",
        verbose_name="Получатель",
        on_delete=models.CASCADE,
    )
    question_text = models.TextField(
        "Текст вопроса",
    )
    answer_text = models.TextField("Текст ответа", null=True, blank=True)
    is_author_notified = models.BooleanField("Автор получил ответ", default=False)
