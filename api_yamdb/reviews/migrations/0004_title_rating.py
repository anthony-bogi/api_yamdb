# Generated by Django 3.2 on 2023-02-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230221_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
