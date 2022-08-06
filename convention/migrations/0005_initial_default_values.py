import datetime
from django.db import migrations


def test_values(apps, schema_editor):
    Attendee = apps.get_model("convention", "Attendee")
    Block = apps.get_model("convention", "Block")
    Event = apps.get_model("convention", "Event")
    Flow = apps.get_model("convention", "Flow")

    Event.objects.create(
        title="Test_event",
        starting_date=datetime.datetime(2022, 8, 9),
        ending_date=datetime.datetime(2022, 8, 10),
    )

    event = Event.objects.get(title="Test_event")

    Flow.objects.create(title="Вступительные мероприятия", event=event)

    Flow.objects.create(title="Поток 'Эверест'", event=event)

    Flow.objects.create(title="Поток 'Альпы'", event=event)

    Flow.objects.create(title="Заключительные мероприятия", event=event)

    Attendee.objects.create(
        telegram_id=12345678,
        event=event,
        telegram_username="Devman",
        firstname="Иван",
        lastname="Иванов",
        company="",
        position="Независимый эксперт",
    )

    Attendee.objects.create(
        telegram_id=11111111,
        event=event,
        telegram_username="Devman",
        firstname="Фёдор",
        lastname="Фёдоров",
        company="Data Insight",
        position="Вице-президент IBF",
    )

    Attendee.objects.create(
        telegram_id=11111112,
        event=event,
        telegram_username="Devman",
        firstname="Денис",
        lastname="Денисов",
        company="FMNT",
        position="Заместитель генерального директора",
    )

    Attendee.objects.create(
        telegram_id=11111113,
        event=event,
        telegram_username="Devman",
        firstname="Борис",
        lastname="Борисов",
        company="Россия Вперед",
        position="Главный консультант",
    )

    Attendee.objects.create(
        telegram_id=11111114,
        event=event,
        telegram_username="Devman",
        firstname="Анна",
        lastname="Аннова",
        company="Lenta",
        position="Исполнительный директор",
    )

    Attendee.objects.create(
        telegram_id=11111115,
        event=event,
        telegram_username="Devman",
        firstname="Сергей",
        lastname="Володин",
        company="Viber",
        position="Руководитель отдела продаж",
    )

    Attendee.objects.create(
        telegram_id=11111116,
        event=event,
        telegram_username="Devman",
        firstname="Михаил",
        lastname="Михалов",
        company="FMDS",
        position="Руководитель направления",
    )

    Attendee.objects.create(
        telegram_id=11111117,
        event=event,
        telegram_username="Devman",
        firstname="Максим",
        lastname="Максимов",
        company="Beelin",
        position="Product manager",
    )

    Attendee.objects.create(
        telegram_id=11111118,
        event=event,
        telegram_username="Devman",
        firstname="Артем",
        lastname="Артемов",
        company="Beta",
        position="Менеджер проектов",
    )

    Attendee.objects.create(
        telegram_id=11111119,
        event=event,
        telegram_username="Devman",
        firstname="Кирилл",
        lastname="Кириенко",
        company="SmartA",
        position="Директор по развитию бизнеса",
    )

    Attendee.objects.create(
        telegram_id=11111120,
        event=event,
        telegram_username="Devman",
        firstname="Дмитрий",
        lastname="Медведев",
        company="Московский УФАС",
        position="Директор юридического департамента",
    )

    Attendee.objects.create(
        telegram_id=11111121,
        event=event,
        telegram_username="Devman",
        firstname="Леся",
        lastname="Самойлова",
        company="SSL",
        position="CEO",
    )

    Attendee.objects.create(
        telegram_id=11111122,
        event=event,
        telegram_username="Devman",
        firstname="Надежда",
        lastname="Бабкина",
        company="Gete",
        position="CEO",
    )

    Attendee.objects.create(
        telegram_id=11111123,
        event=event,
        telegram_username="Devman",
        firstname="Евгений",
        lastname="Евгеньев",
        company="MediaShot",
        position="Генеральный директор",
    )

    Attendee.objects.create(
        telegram_id=11111124,
        event=event,
        telegram_username="Devman",
        firstname="Екатерина",
        lastname="Ворот",
        company="PRRP",
        position="Digital Director",
    )

    Attendee.objects.create(
        telegram_id=11111125,
        event=event,
        telegram_username="Devman",
        firstname="Татьяна",
        lastname="Вилет",
        company="АО 'Програм регион'",
        position="Директор",
    )

    Attendee.objects.create(
        telegram_id=11111126,
        event=event,
        telegram_username="Devman",
        firstname="Артем",
        lastname="Викторов",
        company="АО 'Програм регион'",
        position="Диреткор по цифровым продуктам",
    )

    Attendee.objects.create(
        telegram_id=11111127,
        event=event,
        telegram_username="Devman",
        firstname="Евгений",
        lastname="Валуев",
        company="ДодоП",
        position="Совладелец",
    )

    Attendee.objects.create(
        telegram_id=11111128,
        event=event,
        telegram_username="Devman",
        firstname="Сергей",
        lastname="Кулькин",
        company="1Z",
        position="Заместитель генерального директора",
    )

    Attendee.objects.create(
        telegram_id=11111129,
        event=event,
        telegram_username="Devman",
        firstname="Игорь",
        lastname="Игорев",
        company="Экватор",
        position="Диретор по развитию рекламных продуктов",
    )

    Attendee.objects.create(
        telegram_id=11111130,
        event=event,
        telegram_username="Devman",
        firstname="Дмитрий",
        lastname="Бирюков",
        company="Bot.ru",
        position="Основатель и руководитель",
    )

    Attendee.objects.create(
        telegram_id=11111131,
        event=event,
        telegram_username="Devman",
        firstname="Андрей",
        lastname="Петров",
        company="InSa",
        position="Руководитель клиентского сервиса",
    )

    Attendee.objects.create(
        telegram_id=11111132,
        event=event,
        telegram_username="Devman",
        firstname="Алексей",
        lastname="Петров",
        company="Институт бизнес-программирования",
        position="Директор",
    )

    Attendee.objects.create(
        telegram_id=11111133,
        event=event,
        telegram_username="Devman",
        firstname="Константин",
        lastname="Константинопольский",
        company="eLe",
        position="Эксперт по работе с платным трафиком",
    )

    Attendee.objects.create(
        telegram_id=11111134,
        event=event,
        telegram_username="Devman",
        firstname="Александр",
        lastname="Бродский",
        company="digital-агентство Ant-te",
        position="Руководитель",
    )

    Attendee.objects.create(
        telegram_id=11111135,
        event=event,
        telegram_username="Devman",
        firstname="Алексей",
        lastname="Жирков",
        company="BINANCE",
        position="Основатель",
    )

    Attendee.objects.create(
        telegram_id=11111136,
        event=event,
        telegram_username="Devman",
        firstname="Денис",
        lastname="Глушаков",
        company="Gol Didgital",
        position="Основатель агентства",
    )

    Attendee.objects.create(
        telegram_id=11111137,
        event=event,
        telegram_username="Devman",
        firstname="Дмитрий",
        lastname="Колбин",
        company="BloggerArea",
        position="Директор по развитию бизнеса",
    )

    Attendee.objects.create(
        telegram_id=11111138,
        event=event,
        telegram_username="Devman",
        firstname="Алексей",
        lastname="Пушилин",
        company="ГК КБ",
        position="Директор по развитию",
    )

    flow = Flow.objects.get(title="Вступительные мероприятия")
    moderator = Attendee.objects.get(lastname="Иванов")

    Block.objects.create(
        title="Регистрация",
        description="Регистрация",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 9, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 10, 0, 0),
    )

    Block.objects.create(
        title="Дискуссия – пути развития рынка разработки",
        description="Планерная дискуссия – пути развития рынка разработки",
        moderator=moderator,
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 10, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 11, 30, 0),
    )

    Block.objects.create(
        title="Нетворкинг",
        description="Перерыв, Нетворкинг, участие в зоне эксмпо",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 11, 30, 0),
        ends_at=datetime.datetime(2022, 8, 9, 12, 00, 0),
    )

    flow = Flow.objects.get(title="Поток 'Эверест'")
    moderator = Attendee.objects.get(lastname="Аннова")

    Block.objects.create(
        title="Коммуникационные инновации",
        description="Коммуникационные инновации",
        moderator=moderator,
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 12, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 13, 30, 0),
    )

    Block.objects.create(
        title="Обед",
        description="Обед, Нетворкинг",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 13, 30, 0),
        ends_at=datetime.datetime(2022, 8, 9, 14, 0, 0),
    )

    Block.objects.create(
        title="Построение предективной аналитики",
        description="Построение предективной аналитики",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 14, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 14, 50, 0),
    )

    Block.objects.create(
        title="Автоматизация рекламных коммуникаций",
        description="Автоматизация рекламных коммуникаций",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 14, 50, 0),
        ends_at=datetime.datetime(2022, 8, 9, 15, 40, 0),
    )

    Block.objects.create(
        title="Системы управления коммуникациями компании с клиентами",
        description="Системы управления коммуникациями компании с клиентами",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 15, 40, 0),
        ends_at=datetime.datetime(2022, 8, 9, 16, 30, 0),
    )

    flow = Flow.objects.get(title="Поток 'Альпы'")

    Block.objects.create(
        title="Автоматизация продаж",
        description="Автоматизация продаж",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 12, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 13, 30, 0),
    )

    Block.objects.create(
        title="Нетворкинг",
        description="Обед, Нетворкинг, Участие в зоне экспо",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 13, 30, 0),
        ends_at=datetime.datetime(2022, 8, 9, 14, 0, 0),
    )

    Block.objects.create(
        title="Построение предективной аналитики",
        description="Построение предективной аналитики",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 14, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 14, 30, 0),
    )

    Block.objects.create(
        title="Автоматизация рекламных коммуникаций",
        description="Автоматизация рекламных коммуникаций",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 14, 30, 0),
        ends_at=datetime.datetime(2022, 8, 9, 16, 30, 0),
    )

    flow = Flow.objects.get(title="Заключительные мероприятия")

    Block.objects.create(
        title="Нетворкинг",
        description="Кофе-брейк, Нетворкинг, участие в зоне экспо",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 16, 30, 0),
        ends_at=datetime.datetime(2022, 8, 9, 17, 0, 0),
    )

    Block.objects.create(
        title="Премия 'BMA 2022'",
        description="Награждение сервисов и инструментов автоматизации",
        flow=flow,
        starts_at=datetime.datetime(2022, 8, 9, 17, 0, 0),
        ends_at=datetime.datetime(2022, 8, 9, 18, 0, 0),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("convention", "0004_block_description"),
    ]

    operations = [migrations.RunPython(test_values)]
