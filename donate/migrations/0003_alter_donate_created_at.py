# Generated by Django 3.2 on 2022-08-07 14:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0002_auto_20220807_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donate',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата транзакции'),
        ),
    ]
