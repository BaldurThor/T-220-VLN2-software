# Generated by Django 4.0.4 on 2022-05-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0009_item_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]