# Generated by Django 3.1 on 2022-02-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quest', '0009_auto_20220131_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gestioneinserimento',
            name='passo_corrente',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='gestioneinserimento',
            name='passo_destra',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='gestioneinserimento',
            name='passo_sinistra',
            field=models.CharField(max_length=50),
        ),
    ]
