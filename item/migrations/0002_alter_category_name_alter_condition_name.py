# Generated by Django 4.0.4 on 2022-05-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=191),
        ),
        migrations.AlterField(
            model_name='condition',
            name='name',
            field=models.CharField(max_length=191),
        ),
    ]
