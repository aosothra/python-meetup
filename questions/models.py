from django.db import models
from django.db.models import Q

from convention.models import Attendee

# Create your models here.
class QuestionQuerySet(models.QuerySet):
    def new(self, recipient_id, event):
        return self.filter(
            recipient__telegram_id=recipient_id,
            recipient__event=event,
            is_ignored=False,
        ).filter(Q(answer_text__isnull=True) | Q(answer_text__iexact=""))


class Question(models.Model):
    author = models.ForeignKey(
        Attendee,
        related_name="asked_questions",
        verbose_name="Автор вопроса",
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        Attendee,
        related_name="recieved_questions",
        verbose_name="Спикер",
        on_delete=models.CASCADE,
    )
    question_text = models.TextField(
        "Текст вопроса",
    )
    answer_text = models.TextField("Текст ответа", null=True, blank=True)
    is_author_notified = models.BooleanField("Автор получил ответ", default=False)
    is_ignored = models.BooleanField("Спикер убрал вопрос", default=False)

    objects = QuestionQuerySet.as_manager()
