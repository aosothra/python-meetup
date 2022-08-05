# Generated by Django 3.2 on 2022-08-05 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0005_initial_default_values'),
        ('questions', '0003_alter_question_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_ignored',
            field=models.BooleanField(default=False, verbose_name='Спикер убрал вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved_questions', to='convention.attendee', verbose_name='Спикер'),
        ),
    ]