# Generated by Django 3.1 on 2022-01-31 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0006_auto_20220127_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settore',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]