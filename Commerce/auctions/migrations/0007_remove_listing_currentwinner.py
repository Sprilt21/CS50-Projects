# Generated by Django 3.1 on 2020-12-27 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201227_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='currentWinner',
        ),
    ]
