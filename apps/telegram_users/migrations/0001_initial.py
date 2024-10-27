# Generated by Django 5.0.1 on 2024-10-27 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=255, null=True)),
                ('full_name', models.CharField(max_length=255)),
                ('language', models.CharField(choices=[('ru', 'Ru'), ('uz', 'Uz')], default='uz', max_length=2)),
                ('phone_number', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Telegram Foydalanuvchi ',
                'verbose_name_plural': 'Telegram Foydalanuvchilar ',
            },
        ),
    ]
