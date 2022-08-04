# Generated by Django 3.2 on 2022-08-04 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('convention', '0002_attendee_telegram_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название блока')),
            ],
            options={
                'verbose_name': 'Блок докладов',
                'verbose_name_plural': 'Блоки докладов',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название ивента')),
            ],
            options={
                'verbose_name': 'Ивент',
                'verbose_name_plural': 'Ивенты',
            },
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название выступления')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='convention.block')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentations', to='convention.attendee')),
            ],
            options={
                'verbose_name': 'Выступление',
                'verbose_name_plural': 'Выступления',
            },
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Название потока')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flows', to='convention.event')),
            ],
            options={
                'verbose_name': 'Поток',
                'verbose_name_plural': 'Потоки',
            },
        ),
        migrations.AddField(
            model_name='block',
            name='flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='convention.flow'),
        ),
    ]