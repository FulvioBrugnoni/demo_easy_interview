# Generated by Django 3.1 on 2022-01-27 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0003_auto_20220119_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidatoparametro',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='candidatoparametro',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='candidatoparametro',
            name='giorno',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
