# Generated by Django 3.2 on 2022-08-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_username', models.CharField(blank=True, max_length=32, null=True, verbose_name='Логин в телеграмме')),
                ('amount', models.IntegerField(verbose_name='Сумма')),
                ('currency', models.CharField(default='RUB', max_length=3, verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'Донат',
                'verbose_name_plural': 'Донаты',
            },
        ),
    ]