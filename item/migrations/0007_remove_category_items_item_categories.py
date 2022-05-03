# Generated by Django 4.0.4 on 2022-05-03 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_category_items_delete_categoryitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(to='item.category'),
        ),
    ]