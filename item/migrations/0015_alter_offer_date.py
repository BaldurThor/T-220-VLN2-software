# Generated by Django 4.0.4 on 2022-05-10 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0014_alter_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
