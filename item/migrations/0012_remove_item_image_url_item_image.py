# Generated by Django 4.0.4 on 2022-05-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_item_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image_url',
        ),
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='', upload_to='users'),
            preserve_default=False,
        ),
    ]
