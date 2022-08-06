from datetime import datetime
import json
from django.core.management import BaseCommand
from django.conf import settings
from django.utils import timezone

from convention.models import Attendee, Block, Event, Flow, Presentation


class Command(BaseCommand):
    def set_time(self, time: str, datetime: datetime):
        hour, minute = time.split(":")
        return datetime.replace(hour=int(hour), minute=int(minute), second=0)

    def handle(self, *args, **options):
        now = timezone.now()

        with open("fake_event_map.json", "r") as json_file:
            event_map = json.load(json_file)

        Event.objects.all().delete()
        Flow.objects.all().delete()
        Block.objects.all().delete()
        Attendee.objects.all().delete()
        Presentation.objects.all().delete()

        new_event = Event.objects.create(
            title=f"Фейк-конференция {now.strftime('%Y')}",
            starting_date=now,
            ending_date=now,
        )

        for attendee in event_map["attendees"]:
            company = attendee["company"] if attendee["company"] else new_event.title
            Attendee.objects.create(
                telegram_id=attendee["telegram_id"],
                event=new_event,
                firstname=attendee["firstname"],
                lastname=attendee["lastname"],
                company=company,
                position=attendee["position"],
            )

        for flow in event_map["flows"]:
            new_flow = Flow.objects.create(title=flow["title"], event=new_event)
            for block in flow["blocks"]:
                moderator = (
                    Attendee.objects.get(telegram_id=block["moderator"])
                    if block.get("moderator", None)
                    else None
                )
                new_block = Block.objects.create(
                    title=block["title"],
                    starts_at=self.set_time(block["starts_at"], now),
                    ends_at=self.set_time(block["ends_at"], now),
                    description=block.get("description", None),
                    moderator=moderator,
                    flow=new_flow,
                )
                for presentation in block.get("presentations", []):
                    speakers = Attendee.objects.filter(
                        telegram_id__in=presentation["speakers"]
                    )
                    new_presentation = Presentation.objects.create(
                        title=presentation["title"], block=new_block
                    )
                    new_presentation.speakers.set(speakers)
