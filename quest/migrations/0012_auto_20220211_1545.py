# Generated by Django 3.1 on 2022-02-11 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0011_auto_20220204_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professione',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='settore',
            name='name',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]