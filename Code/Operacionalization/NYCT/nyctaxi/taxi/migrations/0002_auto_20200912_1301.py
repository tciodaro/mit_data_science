# Generated by Django 3.1 on 2020-09-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxi',
            name='idTaxi',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
