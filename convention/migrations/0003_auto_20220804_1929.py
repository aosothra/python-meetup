# Generated by Django 3.2 on 2022-08-04 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0002_alter_block_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moderated_blocks', to='convention.attendee', verbose_name='Модератор'),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название выступления'),
        ),
    ]
