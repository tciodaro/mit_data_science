# Generated by Django 3.0.8 on 2020-09-05 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0018_auto_20200904_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosresult',
            name='din_execucao',
            field=models.DateTimeField(null=True),
        ),
    ]
