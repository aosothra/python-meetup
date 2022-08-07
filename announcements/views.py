from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpRequest, JsonResponse, Http404
from telegram import Bot
from telegram.constants import PARSEMODE_HTML
from telegram.error import BadRequest
from convention.models import Attendee

from .models import Announcement


def announce(request: HttpRequest, anouncement_id: int):
    if not request.user.is_authenticated and not request.user.is_staff:
        return Http404("You are not authorized to do that stuff")

    announcement = Announcement.objects.get(id=anouncement_id)
    announcement.released_on = timezone.now()
    announcement.save()

    bot = Bot(settings.BOT_TOKEN)
    attendees = Attendee.objects.filter(event=announcement.event)

    for attendee in attendees:
        try:
            bot.send_message(
                chat_id=attendee.telegram_id,
                text=render_to_string(
                    "announcement_message.html",
                    context={"message": announcement.message},
                ),
                parse_mode=PARSEMODE_HTML,
            )
        except BadRequest:
            pass

    return JsonResponse({"ok": True})
