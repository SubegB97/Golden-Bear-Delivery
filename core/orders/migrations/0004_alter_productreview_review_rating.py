# Generated by Django 3.2.7 on 2021-11-19 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20211119_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='review_rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]
