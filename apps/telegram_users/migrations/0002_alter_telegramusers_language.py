# Generated by Django 5.0.1 on 2024-10-27 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramusers',
            name='language',
            field=models.CharField(choices=[('ru', 'Ru'), ('uz', 'Uz'), ('en', 'En')], default='uz', max_length=2),
        ),
    ]