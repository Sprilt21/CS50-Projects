# Generated by Django 3.1 on 2021-01-24 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20210122_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.CharField(default='Test', max_length=1000),
            preserve_default=False,
        ),
    ]
